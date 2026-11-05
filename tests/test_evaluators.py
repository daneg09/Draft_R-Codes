import pytest

from rcodes.core import evaluators as ev
from rcodes.core.facts import FactSet

TABLE = {
    "id": "t", "title": "t", "keys": ["site.r_code"], "unit": "%",
    "rows": [{"match": {"site.r_code": "R2-R25"}, "value": 55}, {"match": {"site.r_code": "R30+"}, "value": None}],
    "source": {},
}
TABLE2 = {
    "id": "t2", "title": "t2", "keys": ["site.r_code", "building.storeys"],
    "rows": [{"match": {"site.r_code": "R20-R35", "building.storeys": 1}, "value": 1.0},
             {"match": {"site.r_code": "R20-R35", "building.storeys": {"min": 2}}, "value": 1.5}],
    "default": 2.0, "source": {},
}


def tables(ref):
    return {"t": TABLE, "t2": TABLE2}.get(ref)


def facts(**kw):
    return FactSet(values=kw)


def test_threshold():
    out = ev.evaluate_spec({"type": "threshold", "fact": "a", "op": ">=", "value": 5}, facts(a=5), tables)
    assert out.status == ev.MEETS and out.tested == 5 and out.threshold == 5
    out = ev.evaluate_spec({"type": "threshold", "fact": "a", "op": ">=", "value": 5}, facts(a=4.9), tables)
    assert out.status == ev.DOES_NOT_MEET
    out = ev.evaluate_spec({"type": "threshold", "fact": "a", "op": ">=", "value": 5}, facts(), tables)
    assert out.status == ev.CANNOT_TELL and out.missing == ["a"]
    out = ev.evaluate_spec({"type": "threshold", "fact": "a", "op": "<=", "value": {"fact": "b"}}, facts(a=1), tables)
    assert out.status == ev.CANNOT_TELL and out.missing == ["b"]


def test_boolean_and_count():
    assert ev.evaluate_spec({"type": "boolean", "fact": "x"}, facts(x=True), tables).status == ev.MEETS
    assert ev.evaluate_spec({"type": "boolean", "fact": "x", "expected": False}, facts(x=True), tables).status == ev.DOES_NOT_MEET
    assert ev.evaluate_spec({"type": "count", "fact": "n", "op": ">", "value": 1}, facts(n=2), tables).status == ev.MEETS


def test_percentage_of():
    out = ev.evaluate_spec({"type": "percentage-of", "fact": "roof", "of": "site", "op": "<=", "value": 55},
                           facts(roof=240, site=450), tables)
    assert out.status == ev.MEETS and out.tested == pytest.approx(53.33, abs=0.01)
    out = ev.evaluate_spec({"type": "percentage-of", "fact": "roof", "of": "site", "op": "<=", "value": 55},
                           facts(roof=240, site=0), tables)
    assert out.status == ev.CANNOT_TELL


def test_table_lookup():
    spec = {"type": "table-lookup", "table": "t", "fact": "cover", "op": "<="}
    assert ev.evaluate_spec(spec, FactSet(values={"site.r_code": "R20", "cover": 50}), tables).status == ev.MEETS
    assert ev.evaluate_spec(spec, FactSet(values={"site.r_code": "R20", "cover": 56}), tables).status == ev.DOES_NOT_MEET
    assert ev.evaluate_spec(spec, FactSet(values={"site.r_code": "R30", "cover": 90}), tables).status == ev.NOT_APPLICABLE
    out = ev.evaluate_spec(spec, FactSet(values={"cover": 90}), tables)
    assert out.status == ev.CANNOT_TELL and out.missing == ["site.r_code"]
    spec2 = {"type": "table-lookup", "table": "t2", "fact": "setback", "op": ">="}
    assert ev.evaluate_spec(spec2, FactSet(values={"site.r_code": "R30", "building.storeys": 2, "setback": 1.5}), tables).status == ev.MEETS
    assert ev.evaluate_spec(spec2, FactSet(values={"site.r_code": "R30", "building.storeys": 1, "setback": 1.2}), tables).status == ev.MEETS
    assert ev.evaluate_spec(spec2, FactSet(values={"site.r_code": "R50", "building.storeys": 1, "setback": 1.2}), tables).threshold == 2.0
    with pytest.raises(KeyError):
        ev.evaluate_spec({"type": "table-lookup", "table": "missing", "fact": "x"}, facts(x=1), tables)


def test_formula():
    spec = {"type": "formula", "expr": "garage + house_length + 1.0", "op": "<=", "value": {"fact": "depth"}}
    out = ev.evaluate_spec(spec, facts(garage=5.0, house_length=24.0, depth=30.0), tables)
    assert out.status == ev.MEETS and out.tested == 30.0
    out = ev.evaluate_spec(spec, facts(garage=5.0, house_length=24.5, depth=30.0), tables)
    assert out.status == ev.DOES_NOT_MEET
    out = ev.evaluate_spec(spec, facts(garage=5.0, depth=30.0), tables)
    assert out.status == ev.CANNOT_TELL and out.missing == ["house_length"]
    dotted = {"type": "formula", "expr": "max(site.width_m, 10) * 0.5", "op": ">=", "value": 6}
    assert ev.evaluate_spec(dotted, FactSet(values={"site.width_m": 12.5}), tables).status == ev.MEETS
    with pytest.raises(ValueError):
        ev.evaluate_spec({"type": "formula", "expr": "__import__('os')", "op": ">=", "value": 1}, facts(), tables)


def test_composite():
    spec = {"type": "composite", "mode": "all", "parts": [
        {"type": "boolean", "fact": "p"}, {"type": "count", "fact": "n", "op": ">", "value": 1}]}
    assert ev.evaluate_spec(spec, facts(p=True, n=2), tables).status == ev.MEETS
    assert ev.evaluate_spec(spec, facts(p=False, n=2), tables).status == ev.DOES_NOT_MEET
    out = ev.evaluate_spec(spec, facts(p=True), tables)
    assert out.status == ev.CANNOT_TELL and out.missing == ["n"]
    spec["mode"] = "any"
    assert ev.evaluate_spec(spec, facts(p=False, n=2), tables).status == ev.MEETS


def test_geometry():
    pytest.importorskip("shapely")
    square = {"type": "Polygon", "coordinates": [[[0, 0], [4, 0], [4, 3], [0, 3], [0, 0]]]}
    out = ev.evaluate_spec({"type": "geometry", "measure": "area", "geometry": "g", "op": ">=", "value": 9},
                           facts(g=square), tables)
    assert out.status == ev.MEETS and out.tested == 12.0
    out = ev.evaluate_spec({"type": "geometry", "measure": "min_dimension", "geometry": "g", "op": ">=", "value": 1.5},
                           facts(g=square), tables)
    assert out.status == ev.MEETS and out.tested == 3.0
    site = {"type": "Polygon", "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]}
    out = ev.evaluate_spec({"type": "geometry", "measure": "pct_of", "geometry": "g", "other": "s", "op": "<=", "value": 15},
                           facts(g=square, s=site), tables)
    assert out.status == ev.MEETS and out.tested == 12.0


def test_nominal_and_effect():
    spec = {"type": "threshold", "fact": "a", "op": ">=", "value": 5.0}
    assert ev.nominal_value(spec, facts(), tables) == 5.0
    assert ev.apply_effect(spec, {"set": {"value": 4.5}})["value"] == 4.5
    assert ev.apply_effect(spec, {"replace_evaluator": {"type": "boolean", "fact": "z"}})["type"] == "boolean"
    tl = {"type": "table-lookup", "table": "t", "fact": "cover", "op": "<="}
    assert ev.nominal_value(tl, FactSet(values={"site.r_code": "R20"}), tables) == 55


def test_formula_table_threshold_with_no_row_is_not_applicable():
    loc = {"id": "loc", "title": "loc", "keys": ["site.location"],
           "rows": [{"match": {"site.location": "A"}, "value": "0.1 * n"}, {"match": {"site.location": "B"}, "value": "0.15 * n"}],
           "source": {}}
    spec = {"type": "formula", "expr": "bays", "op": ">=", "value": {"table": "loc"}}
    res = lambda ref: {"loc": loc}.get(ref)
    assert ev.evaluate_spec(spec, FactSet(values={"bays": 2, "n": 10, "site.location": "B"}), res).status == ev.MEETS
    out = ev.evaluate_spec(spec, FactSet(values={"bays": 2, "n": 10}), res)
    assert out.status == ev.CANNOT_TELL and out.missing == ["site.location"]
    assert ev.evaluate_spec(spec, FactSet(values={"bays": 2, "n": 10, "site.location": "C"}), res).status == ev.NOT_APPLICABLE
