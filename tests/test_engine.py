import copy
import json

from rcodes.core import evaluate, lint, report
from rcodes.core import evaluators as ev
from rcodes.core.resolver import NOT_RECOGNISED, RECOGNISED, resolve
from rcodes.core.schema import validate

GARAGE = "rcodes:draft-2026-10-24/ch2/C3.3.3"
COVER = "rcodes:draft-2026-10-24/ch2/C3.1.1"
V = "draft-2026-10-24"


def by_id(res):
    return {r.rule_id: r for r in res.results}


def test_registry_loaded(registry):
    assert registry.package(V, "ch1") and registry.package(V, "ch2")
    assert registry.problems() == []
    assert registry.operation(V).__name__ == "rcodes.chapters.ch1.operation"


def test_application_schema(app_r30):
    assert validate("application", app_r30) == []
    bad = copy.deepcopy(app_r30)
    bad["proposal"]["dwelling_type"] = "castle"
    assert validate("application", bad)


def test_resolve_selects_chapter_and_rules(registry, app_r30):
    res = resolve(registry, app_r30, V)
    assert res.chapter == "ch2"
    assert {e.rule.id for e in res.rules} == {GARAGE, COVER}
    app_r40 = copy.deepcopy(app_r30)
    app_r40["site"]["r_code"] = "R40"
    res = resolve(registry, app_r40, V)
    assert {e.rule.id for e in res.rules} == {COVER}  # garage rule is R2-R35 only


def test_run_meets_and_pathway(registry, app_r30):
    res = evaluate.run(registry, app_r30, V)
    r = by_id(res)
    assert r[GARAGE].status == ev.MEETS and r[GARAGE].outcome["threshold"] == 5.0
    assert r[COVER].status == ev.NOT_APPLICABLE
    assert res.pathway == evaluate.PATHWAY_DEEMED_EXEMPT and res.elements_on_merit == []
    assert res.da["required"] is None  # scheme not checked
    assert res.consultation == []


def test_exception_rescues_and_cannot_tell(registry, app_r30):
    app = copy.deepcopy(app_r30)
    app["parking"]["garage"]["setback_primary_m"] = 4.5
    app["site"]["verge"]["path_or_road_offset_m"] = 1.2
    r = by_id(evaluate.run(registry, app, V))
    assert r[GARAGE].status == ev.MEETS and r[GARAGE].exception_used == "footpath or road more than 1 m from boundary"
    del app["site"]["verge"]
    res = evaluate.run(registry, app, V)
    r = by_id(res)
    assert r[GARAGE].status == ev.CANNOT_TELL
    assert "site.verge.path_or_road_offset_m" in r[GARAGE].missing
    assert res.pathway == evaluate.PATHWAY_UNDETERMINED
    assert "civil design / subdivision engineering drawings" in res.missing
    app["site"]["verge"] = {"path_or_road_offset_m": 0.5}
    r = by_id(evaluate.run(registry, app, V))
    assert r[GARAGE].status == ev.DOES_NOT_MEET and r[GARAGE].fallback.endswith("M3.3.3")
    app["parking"]["garage"].update({"setback_primary_m": 3.0, "parallel_parking": True, "parallel_wall_openings": 2})
    r = by_id(evaluate.run(registry, app, V))
    assert r[GARAGE].status == ev.MEETS and r[GARAGE].exception_used == "garage allows parallel parking"


def test_merit_pathway_and_consultation(registry, app_r30):
    app = copy.deepcopy(app_r30)
    app["site"].update({"r_code": "R20", "area_m2": 450})
    app["building"]["roofed_area_m2"] = 279
    app["parking"]["garage"]["setback_primary_m"] = 6.0
    res = evaluate.run(registry, app, V)
    r = by_id(res)
    assert r[COVER].status == ev.DOES_NOT_MEET and r[COVER].outcome["tested"] == 62.0
    assert res.pathway == evaluate.PATHWAY_MERIT and res.elements_on_merit == ["3.1"]
    assert res.consultation[0]["element_title"] == "Site cover"


def test_confidence_threshold(registry, app_r30):
    app = copy.deepcopy(app_r30)
    app["facts_meta"]["parking.garage.setback_primary_m"]["confidence"] = 0.5
    r = by_id(evaluate.run(registry, app, V))
    assert r[GARAGE].status == ev.CANNOT_TELL
    r = by_id(evaluate.run(registry, app, V, threshold=0.4))
    assert r[GARAGE].status == ev.MEETS


def _with_instrument(app, itype, clause, value, **extra):
    app = copy.deepcopy(app)
    app["site"]["instruments"] = [{
        "type": itype, "ref": "Test instrument", "clauses": [{
            "ref": "cl 4", "targets": [dict({"chapter": "ch2", "clause": clause, "effect": {"set": {"value": value}}}, **extra)]}]}]
    return app


def test_ldp_variation_recognised(registry, app_r30):
    app = _with_instrument(app_r30, "ldp", "C3.3.3", 4.5, reading_confirmed=True)
    app["parking"]["garage"]["setback_primary_m"] = 4.5
    res = evaluate.run(registry, app, V)
    r = by_id(res)
    assert r[GARAGE].status == ev.MEETS and r[GARAGE].outcome["threshold"] == 4.5
    assert r[GARAGE].variation["status"] == RECOGNISED and r[GARAGE].variation["direction"] == "decrease"
    assert res.variations[0]["permission"]["table"].endswith("T2.5B")


def test_lpp_variation_not_recognised(registry, app_r30):
    app = _with_instrument(app_r30, "lpp", "C3.3.3", 4.5)
    app["parking"]["garage"]["setback_primary_m"] = 4.5
    res = evaluate.run(registry, app, V)
    r = by_id(res)
    assert r[GARAGE].status == ev.DOES_NOT_MEET
    assert res.variations[0]["status"] == NOT_RECOGNISED and "WAPC" in res.variations[0]["reason"]
    # with WAPC approval recorded the same LPP variation is recognised
    app = _with_instrument(app_r30, "lpp", "C3.3.3", 4.5, wapc_approved=True)
    app["parking"]["garage"]["setback_primary_m"] = 4.5
    assert by_id(evaluate.run(registry, app, V))[GARAGE].status == ev.MEETS


def test_structure_plan_has_no_rights_but_scheme_is_untabled(registry, app_r30):
    app = _with_instrument(app_r30, "structure_plan", "C3.3.3", 4.5)
    res = evaluate.run(registry, app, V)
    assert res.variations[0]["status"] == NOT_RECOGNISED and "no variation rights" in res.variations[0]["reason"]
    app = _with_instrument(app_r30, "scheme", "C3.3.3", 4.5)
    res = evaluate.run(registry, app, V)
    assert res.variations[0]["status"] == RECOGNISED and res.variations[0]["permission"]["level"] == "untabled"


def test_variation_targets_unknown_clause(registry, app_r30):
    app = _with_instrument(app_r30, "ldp", "C9.9.9", 1)
    res = evaluate.run(registry, app, V)
    assert res.variations[0]["status"] == NOT_RECOGNISED and "no rule" in res.variations[0]["reason"]


def test_exclude_effect(registry, app_r30):
    app = copy.deepcopy(app_r30)
    app["site"]["instruments"] = [{"type": "ldp", "ref": "X", "clauses": [{"ref": "1", "targets": [
        {"chapter": "ch2", "element": "3.3", "effect": {"exclude": True}}]}]}]
    r = by_id(evaluate.run(registry, app, V))
    assert r[GARAGE].status == ev.NOT_APPLICABLE and "excluded" in r[GARAGE].outcome["reason"]


def test_cases_in_fixture_package(registry):
    pkg = registry.package(V, "ch2")
    assert pkg.cases
    for case in pkg.cases:
        res = evaluate.run(registry, case["app"], V)
        r = by_id(res)
        for rid, status in case["expect"]["rules"].items():
            assert r[rid].status == status, case["title"]
        if "pathway" in case["expect"]:
            assert res.pathway == case["expect"]["pathway"], case["title"]
        for rid, label in case["expect"].get("exception", {}).items():
            assert r[rid].exception_used == label
        for name in case["expect"].get("missing_contains", []):
            assert any(name in names for names in res.missing.values())


def test_report_formats(registry, app_r30):
    res = evaluate.run(registry, app_r30, V)
    js = json.loads(report.to_json(res))
    assert js["pathway"] == "deemed-exempt" and js["counts"]["MEETS"] == 1
    md = report.to_markdown(res)
    assert "| 3.3 Street setbacks | C3.3.3 | Meets |" in md


def test_compare_pairs_by_replaces(registry, app_r30):
    out = evaluate.compare(registry, app_r30, [V])
    rels = {p["relation"] for p in out["pairs"]}
    assert "tightened" in rels and out["runs"][V]["pathway"] == "deemed-exempt"


def test_lint_clean_fixture(registry):
    findings = lint.lint(registry)
    errors = [f for f in findings if f.level == lint.ERROR]
    assert errors == [], [str(f) for f in errors]
    assert not [f for f in findings if f.check == "tests"]


def test_lint_catches_problems(registry, tmp_path):
    from rcodes.core.registry import Registry
    from rcodes.core.registry import PKG_ROOT
    import shutil
    bad = tmp_path / "pkg-bad"
    shutil.copytree(registry.package(V, "ch2").root, bad)
    rule = json.loads((bad / "rules" / "3.3" / "C3.3.3.json").read_text(encoding="utf-8"))
    rule["fallback"] = "rcodes:draft-2026-10-24/ch2/M9.9.9"
    rule["evaluator"]["fact"] = "parking.garage.undeclared"
    del rule["replaces"]
    (bad / "rules" / "3.3" / "C3.3.3.json").write_text(json.dumps(rule), encoding="utf-8")
    reg = Registry.load(roots=[], package_dirs=[PKG_ROOT / "chapters" / "ch1", bad])
    checks = {(f.check, f.level) for f in lint.lint(reg)}
    assert ("fallback", lint.ERROR) in checks
    assert ("inputs", lint.WARN) in checks
    assert ("replaces", lint.WARN) in checks


# --- engine fixes from the worked example (2026-11-03) ------------------------------

def _worked_plan_only():
    from pathlib import Path
    from rcodes.core.registry import Registry
    root = Path(__file__).resolve().parents[1]
    app = json.loads((root / "examples" / "two-storey-r20-15x30-plan-only.json").read_text(encoding="utf-8"))
    return Registry.load(strict=False), app


def test_unknown_region_marks_both_twins_uncertain():
    reg, app = _worked_plan_only()
    assert "region" not in app["site"]
    res = evaluate.run(reg, app, V)
    r = {x.rule_id.split("/")[-1]: x for x in res.results if x.chapter == "ch2"}
    perth, regional = r["C2.3.1"], r["C2.3.3"]  # Perth and Peel parking and its regional twin
    for x in (perth, regional):
        assert x.applicability == "uncertain"
        assert "site.region" in x.missing
        assert "applicability uncertain: site.region" in x.notes
    assert regional.status == ev.MEETS  # reported as "meets, if it applies"
    # a rule for all regions is not touched
    assert "site.region" not in r["C3.1.1"].missing and r["C3.1.1"].applicability == "applies"
    # once the region is known, only one twin resolves and it applies outright
    app["site"]["region"] = "regional"
    r = {x.rule_id.split("/")[-1]: x for x in evaluate.run(reg, app, V).results if x.chapter == "ch2"}
    assert "C2.3.1" not in r and r["C2.3.3"].applicability == "applies" and "site.region" not in r["C2.3.3"].missing


def _uncertain(rule_data, missing):
    from rcodes.core.resolver import EffectiveRule
    from rcodes.core.rules import Rule
    rule = Rule(dict({"id": "rcodes:x/ch2/C9.9.9", "version": "x", "chapter": "ch2", "element": "9.9",
                      "kind": "measurable", "column": "C"}, **rule_data))
    return EffectiveRule(rule=rule, evaluator=rule.evaluator, exceptions=[], applicability="uncertain",
                         applicability_missing=missing)


def test_cannot_tell_carries_applicability_fact():
    from rcodes.core.facts import FactSet
    eff = _uncertain({"evaluator": {"type": "threshold", "fact": "building.rear_setback_m", "op": ">=", "value": 3}},
                     ["site.battleaxe"])
    out = evaluate.evaluate_rule(eff, FactSet.from_application({}), lambda ref: None)
    assert out.status == ev.CANNOT_TELL
    assert out.missing == ["building.rear_setback_m", "site.battleaxe"]
    # not applicable: the applicability fact is recorded as a note, not as missing
    eff = _uncertain({"evaluator": {"type": "threshold", "fact": "building.rear_setback_m", "op": ">=", "value": None}},
                     ["site.battleaxe"])
    out = evaluate.evaluate_rule(eff, FactSet.from_application({}), lambda ref: None)
    assert out.status == ev.NOT_APPLICABLE and out.missing == [] and "site.battleaxe" in out.notes


def test_source_hints_cover_new_prefixes():
    expect = {
        "adjoining.r_code": "adjoining lot information: scheme map, survey, neighbour's approved plans",
        "overshadow.pct": "shadow diagram, midday 21 June",
        "privacy.cone_setback_m": "elevations and site plan: cone of vision",
        "site_works.fill_m": "site works plan: levels, retaining",
        "outbuilding.area_m2": "site plan: outbuildings",
        "subdivision.proposed": "subdivision plan or title",
        "ancillary.floor_area_m2": "floor plan: ancillary dwelling",
        "landscape.soft_pct": "landscape plan",
        "site.verge.path_or_road_offset_m": "civil design / subdivision engineering drawings",
        "site.region": "lot plan / certificate of title / scheme map",
    }
    results = [evaluate.RuleResult(rule_id=k, chapter="ch2", element="0", element_title="", title="", column="C",
                                   kind="measurable", status=ev.CANNOT_TELL, missing=[k]) for k in expect]
    grouped = evaluate.group_missing(results)
    for name, src in expect.items():
        assert name in grouped.get(src, []), name
    assert "unknown source" not in grouped
    # specific prefixes are listed before the general ones they share a start with
    prefixes = [p for p, _ in evaluate.SOURCE_HINTS]
    for i, p in enumerate(prefixes):
        assert not any(p.startswith(q) for q in prefixes[:i]), p


def test_null_threshold_beats_missing_tested_value():
    from rcodes.core.facts import FactSet
    table = {"id": "t", "keys": ["site.r_code"], "rows": [{"match": {"site.r_code": "R20"}, "value": None}]}
    tables = {"t": table}.get
    facts = FactSet.from_application({"site": {"r_code": "R20"}})
    specs = [
        {"type": "threshold", "fact": "building.rear_setback_m", "value": {"table": "t"}},
        {"type": "count", "fact": "building.walls", "op": "<=", "value": {"table": "t"}},
        {"type": "percentage-of", "fact": "building.roofed_area_m2", "of": "site.area_m2", "value": {"table": "t"}},
        {"type": "formula", "expr": "building.rear_setback_m * 2", "op": ">=", "value": {"table": "t"}},
        {"type": "table-lookup", "table": "t", "fact": "building.rear_setback_m"},
    ]
    for spec in specs:
        assert ev.evaluate_spec(spec, facts, tables).status == ev.NOT_APPLICABLE, spec["type"]
    # an unknown threshold (key fact missing) still gives cannot tell, naming the key fact
    blank = FactSet.from_application({})
    for spec in specs:
        out = ev.evaluate_spec(spec, blank, tables)
        assert out.status == ev.CANNOT_TELL and "site.r_code" in out.missing, spec["type"]


def test_table_1_1_note_only_for_its_codings(registry, app_r30):
    from rcodes.core.facts import FactSet
    op = registry.operation(V)
    a = op.applicability(FactSet.from_application({"site": {"r_code": "R20"}, "proposal": {"dwelling_type": "single_house"}}))
    assert a["chapter"] == "ch2" and not any("R100" in r for r in a["reasons"])
    a = op.applicability(FactSet.from_application({"site": {"r_code": "R160"}, "proposal": {"dwelling_type": "single_house"}}))
    assert any(r.startswith("Note:") and "R160" in r for r in a["reasons"])
