"""Shared checks for the dwelling chapters (ch2 single houses, ch3 grouped dwellings,
ch4p1 apartments R10 to R60).

Each chapter's test module builds its registry and calls these functions with
(registry, version, chapter, summary table id, dwelling_type, report path):

  check_loads             no schema problems; the package has a reasonable number of rules
  check_lint              no ERROR findings
  check_fallbacks         every element in meta.json has a fallback record (M, or the
                          column meta.json "columns.fallback" names, e.g. O for ch4p2)
  check_cases             authored test cases give the expected statuses and pathway
  check_regeneration      the summary table (Table 2A / 3A) regenerates from the rules

The regeneration check (spec section 11): for every metric and coding in the published
summary table, find the rule that governs that metric, evaluate it with probe facts, and
compare the threshold it applies with the table's value. A mismatch is either a
transcription error or a draft inconsistency; both are worth knowing, so mismatches are
reported in full and the check fails only on metrics not flagged `verify` in the table.
"""

from __future__ import annotations

import json
from pathlib import Path

from rcodes.core import codings, evaluate, lint
from rcodes.core import evaluators as ev
from rcodes.core.evaluators import lookup_table
from rcodes.core.facts import FactSet
from rcodes.core.registry import Registry
from rcodes.core.resolver import EffectiveRule


def check_loads(reg: Registry, version: str, chapter: str, min_rules: int = 40) -> None:
    assert reg.problems() == [], "\n".join(reg.problems())
    pkg = reg.package(version, chapter)
    assert pkg is not None, f"package {version}/{chapter} not loaded"
    assert len(pkg.rules) >= min_rules, f"only {len(pkg.rules)} rules"


def check_lint(reg: Registry) -> list:
    """Assert no ERROR findings; return all findings for callers that want the warnings."""
    findings = lint.lint(reg)
    errors = [str(f) for f in findings if f.level == lint.ERROR]
    assert errors == [], "\n".join(errors)
    return findings


def check_fallbacks(reg: Registry, version: str, chapter: str) -> None:
    """A performance chapter (ch4p2) keeps O and DG records in fallbacks/; only the column
    meta.json names as the fallback (O) covers an element."""
    pkg = reg.package(version, chapter)
    column = (pkg.meta.get("columns") or {}).get("fallback", "M")
    elements = set(pkg.meta["elements"])
    have = {r.element for r in pkg.fallbacks.values() if r.column == column}
    missing = sorted(elements - have)
    assert missing == [], f"elements without an {column} record: {missing}"


def check_cases(reg: Registry, version: str, chapter: str) -> None:
    pkg = reg.package(version, chapter)
    assert pkg.cases, "no test cases"
    failures = []
    for case in pkg.cases:
        res = evaluate.run(reg, case["app"], version)
        by_id = {r.rule_id: r for r in res.results}
        for rid, status in (case.get("expect") or {}).get("rules", {}).items():
            got = by_id.get(rid)
            if got is None:
                failures.append(f"{case['title']}: {rid} did not resolve (not applicable to the case's coding/type?)")
            elif got.status != status:
                failures.append(f"{case['title']}: {rid} expected {status}, got {got.status} "
                                f"{json.dumps(got.outcome)} missing={got.missing}")
        # compared as-is: any value evaluate.py produces (deemed-exempt, merit-assessment,
        # performance-assessment, undetermined) is a valid expectation
        if "pathway" in case.get("expect", {}) and res.pathway != case["expect"]["pathway"]:
            failures.append(f"{case['title']}: pathway expected {case['expect']['pathway']}, got {res.pathway}")
    assert failures == [], "\n".join(failures)


# --- summary table regeneration ----------------------------------------------------------

# metric in the summary table -> spec:
#   element  element whose rules may govern the metric
#   facts    evaluator facts that identify the governing rule (a rule matches when any leaf of
#            its evaluator, including parts nested in a composite, tests one of these facts)
#   ops      comparison direction the summary value represents (minimum ">=", maximum "<=");
#            separates e.g. the min-2 and max-4 storey parts of the R100-SL composite
#   probe    facts that satisfy the governing rules' conditions (and keep sibling rules out)
#   codes    optional: restrict the check to these codings
_BW = {"building.boundary_walls.max_height_m": 1, "building.boundary_walls.count": 1,
       "site.frontage_m": 15, "site.access_from_rear_row": False,
       "building.boundary_walls.behind_street_setback": True,
       "building.boundary_walls.adjoining_wall_exists": False, "adjoining.all_coded_r100_sl": True}
_ROW = {"building.row_setback_m": 50, "site.has_row": True}
# side setback bands apply where the building has walls in the band (presence facts, not max wall height)
_WALLS_LOW = {"building.has_walls_to_3_5m": True, "building.has_walls_3_6_to_7m": False, "building.has_walls_over_7_1m": False}
_WALLS_MID = {"building.has_walls_to_3_5m": False, "building.has_walls_3_6_to_7m": True, "building.has_walls_over_7_1m": False}
_WALLS_HIGH = {"building.has_walls_to_3_5m": False, "building.has_walls_3_6_to_7m": False, "building.has_walls_over_7_1m": True}
METRICS = {
    "soft_landscaping_pct": {"element": "1.2", "facts": {"landscape.soft_area_m2"}, "ops": {">="},
                             "probe": {"landscape.soft_area_m2": 50, "landscape.soft_min_dim_m": 2,
                                       "site.significant_tree_retained": False}},
    "site_cover_pct": {"element": "3.1", "facts": {"building.roofed_area_m2"}, "ops": {"<="},
                       "probe": {"building.roofed_area_m2": 100}},
    "storeys": {"element": "3.2", "facts": {"proposal.storeys"}, "ops": {"<="},
                "probe": {"proposal.storeys": 2}},
    "total_height_m": {"element": "3.2", "facts": {"building.total_height_m"}, "ops": {"<="},
                       "probe": {"building.total_height_m": 5}},
    "primary_street_m": {"element": "3.3", "facts": {"building.primary_street_setback_m"}, "ops": {">="},
                         "probe": {"building.primary_street_setback_m": 50, "site.corner_lot_subdivided": False}},
    "secondary_street_m": {"element": "3.3", "facts": {"building.secondary_street_setback_m"}, "ops": {">="},
                           "probe": {"building.secondary_street_setback_m": 50, "site.has_secondary_street": True,
                                     "site.corner_lot": True}},
    "laneway_not_primary_m": {"element": "3.3", "facts": {"building.row_setback_m"}, "ops": {">="},
                              "probe": {**_ROW, "site.row_is_primary_street": False}},
    "laneway_primary_m": {"element": "3.3", "facts": {"building.row_setback_m"}, "ops": {">="},
                          "probe": {**_ROW, "site.row_is_primary_street": True}},
    # flat side setback at R2/R2.5 (the summary table merges one value across all wall heights)
    "side_setback_m": {"element": "3.4", "facts": {"building.side_setback_walls_to_3_5m_m"}, "ops": {">="},
                       "probe": {"building.side_setback_walls_to_3_5m_m": 50, **_WALLS_LOW},
                       "codes": ["R2", "R2.5"]},
    "side_setback_to_3_5m_m": {"element": "3.4", "facts": {"building.side_setback_walls_to_3_5m_m"}, "ops": {">="},
                               "probe": {"building.side_setback_walls_to_3_5m_m": 50, **_WALLS_LOW}},
    "side_setback_3_6_to_7m_m": {"element": "3.4", "facts": {"building.side_setback_walls_3_6_to_7m_m"}, "ops": {">="},
                                 "probe": {"building.side_setback_walls_3_6_to_7m_m": 50, **_WALLS_MID}},
    "side_setback_over_7_1m_m": {"element": "3.4", "facts": {"building.side_setback_walls_over_7_1m_m"}, "ops": {">="},
                                 "probe": {"building.side_setback_walls_over_7_1m_m": 50, **_WALLS_HIGH}},
    "rear_setback_m": {"element": "3.4", "facts": {"building.rear_setback_m"}, "ops": {">="},
                       "probe": {"building.rear_setback_m": 50}},
    "boundary_wall_height_m": {"element": "3.4", "facts": {"building.boundary_walls.max_height_m"}, "ops": {"<="},
                               "probe": _BW},
}
CODES = codings.NUMERIC + ["R100-SL"]


def base_facts(dwelling_type: str) -> dict:
    """Probe base shared by every metric; only the dwelling type differs between chapters."""
    return {"proposal.dwelling_type": dwelling_type, "site.region": "regional", "site.area_m2": 400,
            "site.frontage_m": 15, "proposal.storeys": 1, "building.storeys": 1}


_DEFAULT_OP = {"threshold": ">=", "count": ">=", "percentage-of": "<=", "table-lookup": "<=",
               "formula": ">=", "geometry": ">="}


def _leaves(spec):
    """Yield (path, leaf) for every non-composite part of an evaluator spec; path indexes
    nested composite parts."""
    if spec.get("type") == "composite":
        for i, p in enumerate(spec.get("parts") or []):
            for path, leaf in _leaves(p):
                yield (i, *path), leaf
    else:
        yield (), spec


def _governing(pkg, element, want, code, facts, tables):
    """Rules of `element` that govern a summary-table metric at `code`, as (rule, paths) pairs.

    Any rule with an evaluator is a candidate whatever its column (C in Chapters 2 to 4 Part 1,
    A in the performance chapter). A rule governs when it applies to the coding, every one of its conditions is MEETS on the
    probe facts, and some leaf of its evaluator tests one of the metric's facts in the
    metric's direction (`ops`). Matching looks inside composites, so the R100-SL variants
    (soft landscaping: 10% area AND 1 m dimension; storeys: min 2 AND max 4) are found
    through the part that carries the metric, and `paths` records which parts those are so
    their thresholds can be read from the composite outcome. Threshold, percentage-of and
    table-lookup leaves all match on their tested `fact`, whatever table supplies the value.
    """
    out = []
    for r in pkg.rules_for_element(element):
        spec = r.evaluator or {}
        if not spec or not r.applies_to_code(code):
            continue
        paths = [path for path, leaf in _leaves(spec)
                 if leaf.get("fact") in want["facts"]
                 and leaf.get("op", _DEFAULT_OP.get(leaf.get("type"))) in want["ops"]]
        if not paths:
            continue
        if all(ev.evaluate_spec(c, facts, tables).status == ev.MEETS for c in r.conditions):
            out.append((r, paths))
    return out


def _leaf_value(outcome: dict):
    if outcome.get("status") == ev.NOT_APPLICABLE:
        return None
    if outcome.get("status") == ev.CANNOT_TELL:
        return f"CANNOT_TELL({','.join(outcome.get('missing', []))})"
    return outcome.get("threshold")


def _thresholds(outcome: dict, paths):
    """Threshold applied by each matched leaf; a composite outcome lists its parts in order."""
    vals = set()
    for path in paths:
        o = outcome
        for i in path:
            parts = (o.get("detail") or {}).get("parts")
            if parts is None:
                break
            o = parts[i]
        vals.add(_leaf_value(o))
    return vals


def check_regeneration(reg: Registry, version: str, chapter: str, table_id: str,
                       dwelling_type: str, report_path: Path, codes: list[str] | None = None,
                       metrics: dict | None = None) -> None:
    """`metrics`: metric -> spec mapping (default METRICS); a chapter whose summary table uses
    other metric names supplies its own. `codes`: codings to probe (default: all numeric codes plus R100-SL). A chapter that
    covers only part of the coding range passes its own range; a metric's own `codes` list
    is intersected with it, so nothing outside the chapter's range is probed. A metric with
    no row at all in the summary table is omitted for that chapter (listed in the report)."""
    codes = list(CODES if codes is None else codes)
    metrics = METRICS if metrics is None else metrics
    pkg = reg.package(version, chapter)
    summary = pkg.table(table_id)
    tables = reg.table_resolver(version, chapter)
    base = base_facts(dwelling_type)
    in_table = {(row.get("match") or {}).get("metric") for row in summary.get("rows", [])}
    mismatches, hard, omitted = [], [], []
    for metric, want in metrics.items():
        if metric not in in_table:
            omitted.append(f"{metric}: no rows in {table_id}; not checked")
            continue
        for code in [c for c in want.get("codes", codes) if c in codes]:
            facts = FactSet(values={**base, **want["probe"], "site.r_code": code})
            published, _, row = lookup_table(summary, FactSet(values={"site.r_code": code, "metric": metric}))
            flagged = bool(row and row.get("verify"))
            governing = _governing(pkg, want["element"], want, code, facts, tables)
            clauses = [r.id.split(f"/{chapter}/")[-1] for r, _ in governing]
            if not governing:
                if published is None and not flagged:
                    continue  # no provision in the table and no rule: they agree
                msg = f"{metric} {code}: table says {published!r}; no governing rule found"
                (mismatches if flagged else hard).append(msg)
                continue
            derived = set()
            for r, paths in governing:
                res = evaluate.evaluate_rule(EffectiveRule(rule=r, evaluator=r.evaluator, exceptions=[]), facts, tables)
                derived |= _thresholds(res.outcome, paths)
            if derived != {published}:
                msg = f"{metric} {code}: table says {published!r}; rules {clauses} give {sorted(map(str, derived))}"
                (mismatches if flagged else hard).append(msg)
            elif flagged and row:
                mismatches.append(f"{metric} {code}: table says {published!r}; rules {clauses} agree (row flagged verify)")
    lines = ["HARD (unflagged) mismatches:"] + hard + ["", "Flagged / informational:"] + mismatches
    if omitted:
        lines += ["", "Omitted metrics:"] + omitted
    report = "\n".join(lines)
    Path(report_path).write_text(report + "\n", encoding="utf-8", newline="\n")
    assert hard == [], report
