"""The published worked example (edition/worked/two-storey-r20-15x30.md) stays pinned to the rules.

Runs both application documents through the engine and checks the outcomes the worked example reports,
and checks both documents against the published application JSON Schema.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from rcodes.core import evaluate
from rcodes.core import evaluators as ev
from rcodes.core.facts import FactSet
from rcodes.core.registry import Registry

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
SCHEMA = ROOT / "edition" / "schema" / "application.schema.json"
WORKED = ROOT / "edition" / "worked" / "two-storey-r20-15x30.md"
V = "draft-2026-10-24"
P = f"rcodes:{V}/ch2/"
FILES = {"plan-only": "two-storey-r20-15x30-plan-only.json", "scenario": "two-storey-r20-15x30-scenario.json"}


@pytest.fixture(scope="module")
def reg() -> Registry:
    return Registry.load(strict=False)


def _app(name: str) -> dict:
    return json.loads((EXAMPLES / FILES[name]).read_text(encoding="utf-8"))


def _run(reg, name):
    res = evaluate.run(reg, _app(name), V)
    return res, {r.rule_id[len(P):]: r for r in res.results if r.rule_id.startswith(P)}


@pytest.mark.parametrize("name", sorted(FILES))
def test_validates_against_schema(name):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(jsonschema.validators.validator_for(schema)(schema).iter_errors(_app(name)), key=str)
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("name", sorted(FILES))
def test_every_fact_has_provenance(name):
    app = _app(name)
    meta = app["facts_meta"]
    facts = FactSet.from_application(app)
    for key, m in meta.items():
        assert m["method"] in ("stated", "measured", "computed", "inferred", "assumed"), key
        assert 0 <= m["confidence"] <= 1 and m.get("source"), key
        if name == "scenario" and m["method"] == "assumed" and m["confidence"] == 1.0:
            assert m["note"].startswith("scenario assumption"), key
    assert facts is not None


def test_scenario_extends_plan_only_consistently():
    plan, scen = _app("plan-only"), _app("scenario")

    def flat(d, pre=""):
        out = {}
        for k, v in d.items():
            if isinstance(v, dict):
                out.update(flat(v, f"{pre}{k}."))
            else:
                out[f"{pre}{k}"] = v
        return out

    fp, fs = flat({k: v for k, v in plan.items() if k != "facts_meta"}), flat({k: v for k, v in scen.items() if k != "facts_meta"})
    for k, v in fp.items():
        if k != "site.id":
            assert fs[k] == v, k
            assert scen["facts_meta"].get(k, plan["facts_meta"].get(k)) == plan["facts_meta"].get(k), k
    # every scenario-only fact is a declared assumption
    for k in set(fs) - set(fp):
        m = scen["facts_meta"][k]
        assert m["method"] == "assumed" and m["note"].startswith("scenario assumption"), k
    assert fs["building.rear_setback_m"] == pytest.approx(30 - 6.0 - 20.39)
    assert 1.5 + fs["building.house_width_m"] + 3.4 == pytest.approx(fs["site.width_m"])


def test_plan_only_outcomes(reg):
    res, r = _run(reg, "plan-only")
    assert res.chapter == "ch2" and res.pathway == "undetermined" and res.elements_on_merit == []
    meets = {k for k, x in r.items() if x.status == ev.MEETS}
    assert meets == {"C2.3.3", "C3.1.1", "C3.2.1#storeys", "C3.4.2", "C3.6.1", "C3.6.3",
                     "C4.1.1", "C4.1.1-r2", "C4.1.1-r3"}
    assert not any(x.status == ev.DOES_NOT_MEET for x in r.values())
    assert r["C3.1.1"].outcome["tested"] == pytest.approx(42.89, abs=0.01)
    assert r["C3.6.3"].outcome["tested"] == pytest.approx(38.87, abs=0.01)
    for k in ("C3.3.1", "C3.3.3", "C3.4.1#side-to-3.5m", "C1.2.1", "C2.3.1", "C3.2.1#height"):
        assert r[k].status == ev.CANNOT_TELL, k
    # null-threshold fix: no rear provision at R20, so not applicable even with the rear setback unknown
    assert r["C3.4.1#rear-r17.5"].status == ev.NOT_APPLICABLE
    # unknown region: both parking twins resolve, each "if it applies" with site.region missing
    assert r["C2.3.3"].applicability == "uncertain" and "site.region" in r["C2.3.3"].missing
    assert r["C2.3.1"].status == ev.CANNOT_TELL and "site.region" in r["C2.3.1"].missing
    assert sum(1 for x in r.values() if x.status == ev.CANNOT_TELL) == 78


def test_scenario_outcomes(reg):
    res, r = _run(reg, "scenario")
    assert res.pathway == "undetermined" and res.elements_on_merit == []
    assert res.da["required"] is False
    meets = {k for k, x in r.items() if x.status == ev.MEETS}
    assert meets == {"C1.1.2", "C2.3.3", "C3.1.1", "C3.2.1#storeys", "C3.3.1", "C3.3.2(iii)", "C3.3.3",
                     "C3.4.1#side-3.6-to-7m", "C3.4.1#side-to-3.5m", "C3.4.2", "C3.4.4#count-r20-r25",
                     "C3.6.1", "C3.6.3", "C4.1.1", "C4.1.1-r3"}
    assert not any(x.status == ev.DOES_NOT_MEET for x in r.values())
    assert r["C3.4.1#rear-r17.5"].status == ev.NOT_APPLICABLE
    assert r["C3.3.1"].outcome["threshold"] == 6
    assert r["C3.4.1#side-3.6-to-7m"].outcome["threshold"] == 1.5
    assert r["C3.4.1#side-over-7.1m"].status == ev.CANNOT_TELL
    assert "C2.3.1" not in r  # Perth and Peel parking excluded for a regional site
    assert sum(1 for x in r.values() if x.status == ev.CANNOT_TELL) == 48


def test_worked_example_published():
    text = WORKED.read_text(encoding="utf-8")
    for head in ("## The brief and the plan", "## Plan-only assessment", "## The scenario", "## Scenario assessment",
                 "### Draft ambiguities encountered", "## Summary", "## How to reproduce"):
        assert head in text, head
    for name in ("plan-only", "scenario"):
        assert (WORKED.parent / f"two-storey-r20-15x30-{name}.report.json").exists()
    for entry in ("README.md", "llms.txt"):
        assert "worked/two-storey-r20-15x30.md" in (ROOT / "edition" / entry).read_text(encoding="utf-8"), entry
