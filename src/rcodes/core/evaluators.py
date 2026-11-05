"""Evaluator types. Each takes an evaluator spec, a FactSet and a table resolver and
returns an Outcome. No evaluator calls a model or the network.

Statuses
    MEETS, DOES_NOT_MEET      the test ran
    CANNOT_TELL               a needed fact is unknown; `missing` names it
    NOT_APPLICABLE            the table has no provision for this case (value null)
"""

from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass, field
from typing import Any, Callable

from . import codings
from .facts import UNKNOWN, FactSet

MEETS = "MEETS"
DOES_NOT_MEET = "DOES_NOT_MEET"
CANNOT_TELL = "CANNOT_TELL"
NOT_APPLICABLE = "NOT_APPLICABLE"
NOT_EVALUATED = "NOT_EVALUATED"

_OPS: dict[str, Callable[[Any, Any], bool]] = {
    ">=": operator.ge, "<=": operator.le, ">": operator.gt, "<": operator.lt,
    "==": operator.eq, "!=": operator.ne,
}

TableResolver = Callable[[str], dict[str, Any] | None]


@dataclass
class Outcome:
    status: str
    tested: Any = None
    threshold: Any = None
    op: str | None = None
    missing: list[str] = field(default_factory=list)
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {"status": self.status}
        if self.tested is not None:
            d["tested"] = self.tested
        if self.threshold is not None:
            d["threshold"] = self.threshold
        if self.op:
            d["op"] = self.op
        if self.missing:
            d["missing"] = list(self.missing)
        if self.detail:
            d["detail"] = dict(self.detail)
        return d


def _unknown(*names: str) -> Outcome:
    return Outcome(CANNOT_TELL, missing=[n for n in names if n])


def _resolve_value(v: Any, facts: FactSet, tables: TableResolver | None = None) -> tuple[Any, str | None]:
    """A spec value may be a literal, {"fact": name} or {"table": ref}.
    Returns (value, missing_name). A table miss returns None (no provision)."""
    if isinstance(v, dict) and "fact" in v:
        got = facts.get(v["fact"])
        return (got, v["fact"] if got is UNKNOWN else None)
    if isinstance(v, dict) and "table" in v:
        if tables is None or tables(v["table"]) is None:
            raise KeyError(f"table not found: {v['table']}")
        val, missing, _ = lookup_table(tables(v["table"]), facts)
        if val is UNKNOWN:
            return UNKNOWN, missing[0]
        return val, None
    return v, None


def _compare(tested: Any, op: str, threshold: Any) -> Outcome:
    ok = _OPS[op](tested, threshold)
    return Outcome(MEETS if ok else DOES_NOT_MEET, tested=tested, threshold=threshold, op=op)


# --- individual evaluators -------------------------------------------------

def ev_threshold(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    tested = facts.get(spec["fact"])
    threshold, miss = _resolve_value(spec["value"], facts, tables)
    if threshold is None:  # no provision: the tested fact does not matter
        return Outcome(NOT_APPLICABLE, detail={"reason": "no provision for this case"})
    missing = [n for n, v in ((spec["fact"], tested), (miss, threshold)) if n and v is UNKNOWN]
    if missing:
        return _unknown(*missing)
    return _compare(tested, spec.get("op", ">="), threshold)


ev_count = ev_threshold


def ev_boolean(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    got = facts.get(spec["fact"])
    if got is UNKNOWN:
        return _unknown(spec["fact"])
    expected = spec.get("expected", True)
    return Outcome(MEETS if bool(got) == expected else DOES_NOT_MEET, tested=got, threshold=expected, op="==")


def ev_percentage_of(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    part = facts.get(spec["fact"])
    whole = facts.get(spec["of"])
    threshold, miss = _resolve_value(spec["value"], facts, tables)
    if threshold is None:  # no provision: the tested facts do not matter
        return Outcome(NOT_APPLICABLE, detail={"reason": "no provision for this case"})
    missing = [n for n, v in ((spec["fact"], part), (spec["of"], whole), (miss, threshold)) if n and v is UNKNOWN]
    if missing:
        return _unknown(*missing)
    if not whole:
        return Outcome(CANNOT_TELL, missing=[spec["of"]], detail={"reason": "divisor is zero"})
    pct = 100.0 * float(part) / float(whole)
    out = _compare(round(pct, 2), spec.get("op", "<="), threshold)
    out.detail = {"part": part, "of": whole, "unit": "%"}
    return out


def lookup_table(table: dict[str, Any], facts: FactSet) -> tuple[Any, list[str], dict | None]:
    """Return (value, missing, row). value is UNKNOWN when a key fact is missing,
    NOT_APPLICABLE sentinel (None) when no row matches and no default."""
    key_vals = {}
    missing = []
    for k in table["keys"]:
        v = facts.get(k)
        if v is UNKNOWN:
            missing.append(k)
        key_vals[k] = v
    if missing:
        return UNKNOWN, missing, None
    for row in table["rows"]:
        if all(_match_key(k, key_vals.get(k), want) for k, want in row["match"].items()):
            return row["value"], [], row
    if "default" in table:
        return table["default"], [], None
    return None, [], None


def _match_key(key: str, have: Any, want: Any) -> bool:
    if isinstance(want, list):
        return any(_match_key(key, have, w) for w in want)
    if key.endswith("r_code") and isinstance(have, str) and isinstance(want, str):
        return codings.in_band(have, want)
    if isinstance(want, dict) and ("min" in want or "max" in want):
        try:
            x = float(have)
        except (TypeError, ValueError):
            return False
        return (want.get("min", float("-inf")) <= x <= want.get("max", float("inf")))
    return have == want


def ev_table_lookup(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    table = tables(spec["table"])
    if table is None:
        raise KeyError(f"table not found: {spec['table']}")
    threshold, missing, row = lookup_table(table, facts)
    if threshold is UNKNOWN:
        return _unknown(*missing)
    if threshold is None:
        return Outcome(NOT_APPLICABLE, detail={"table": spec["table"], "reason": "no provision for this case"})
    if "fact" not in spec:  # the lookup value itself is the answer (used by conditions)
        return Outcome(MEETS if bool(threshold) else DOES_NOT_MEET, tested=threshold, detail={"table": spec["table"]})
    tested = facts.get(spec["fact"])
    if tested is UNKNOWN:
        return _unknown(spec["fact"])
    out = _compare(tested, spec.get("op", "<="), threshold)
    out.detail = {"table": spec["table"], "row": row.get("match") if row else "default",
                  "unit": table.get("unit")}
    return out


_ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load,
                  ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd, ast.Call, ast.Pow,
                  ast.IfExp, ast.Compare, ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq,
                  ast.BoolOp, ast.And, ast.Or, ast.Not)
_FUNCS = {"min": min, "max": max, "abs": abs, "round": round}


def safe_eval(expr: str, facts: FactSet) -> tuple[Any, list[str]]:
    """Arithmetic over fact names. Returns (value, missing). Names may use dots."""
    tree = ast.parse(rewrite_dotted(expr), mode="eval")
    missing: list[str] = []

    def check(node: ast.AST) -> None:
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"disallowed expression node: {type(node).__name__}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
                raise ValueError("only min/max/abs/round calls are allowed")
        for child in ast.iter_child_nodes(node):
            check(child)

    check(tree)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id not in _FUNCS}
    env: dict[str, Any] = dict(_FUNCS)
    for n in sorted(names):  # stable order of missing facts across runs
        fact_name = n.replace("__DOT__", ".")
        v = facts.get(fact_name)
        if v is UNKNOWN:
            missing.append(fact_name)
        env[n] = v
    if missing:
        return UNKNOWN, missing
    return eval(compile(tree, "<formula>", "eval"), {"__builtins__": {}}, env), []  # noqa: S307 (AST-whitelisted)


_DOTTED = re.compile(r"(?<![\w.])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+)")


def rewrite_dotted(expr: str) -> str:
    """site.width_m -> site__DOT__width_m so dotted fact names parse as Python names.
    Numeric literals such as 1.0 are untouched."""
    return _DOTTED.sub(lambda m: m.group(1).replace(".", "__DOT__"), expr)


def ev_formula(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    tested, missing = safe_eval(spec["expr"], facts)
    if "value" not in spec and "op" not in spec:
        if tested is UNKNOWN:
            return _unknown(*missing)
        return Outcome(MEETS if bool(tested) else DOES_NOT_MEET, tested=tested, detail={"expr": spec["expr"]})
    threshold, miss = _resolve_value(spec["value"], facts, tables)
    if threshold is None:  # no provision: the tested expression does not matter
        return Outcome(NOT_APPLICABLE, detail={"reason": "no provision for this case"})
    if threshold is UNKNOWN or tested is UNKNOWN:
        return _unknown(*((missing if tested is UNKNOWN else []) + ([miss or "value"] if threshold is UNKNOWN else [])))
    if isinstance(threshold, str):  # threshold may itself be an expression
        threshold, miss2 = safe_eval(threshold, facts)
        if threshold is UNKNOWN:
            return _unknown(*miss2)
    out = _compare(tested, spec.get("op", ">="), threshold)
    out.detail = {"expr": spec["expr"]}
    return out


def ev_geometry(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    try:
        from shapely.geometry import shape
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("geometry evaluators need shapely (pip install rcodes[geometry])") from e
    g = facts.get(spec["geometry"])
    if g is UNKNOWN:
        return _unknown(spec["geometry"])
    geom = shape(g)
    measure = spec["measure"]
    other = None
    if measure in ("intersects", "intersection_area", "pct_of"):
        o = facts.get(spec["other"])
        if o is UNKNOWN:
            return _unknown(spec["other"])
        other = shape(o)
    if measure == "area":
        tested = round(geom.area, 3)
    elif measure == "min_dimension":
        rect = geom.minimum_rotated_rectangle
        xs, ys = rect.exterior.coords.xy
        import math
        sides = [math.dist((xs[i], ys[i]), (xs[i + 1], ys[i + 1])) for i in range(2)]
        tested = round(min(sides), 3)
    elif measure == "intersects":
        return Outcome(MEETS if geom.intersects(other) == spec.get("expected", True) else DOES_NOT_MEET,
                       tested=geom.intersects(other))
    elif measure == "intersection_area":
        tested = round(geom.intersection(other).area, 3)
    elif measure == "pct_of":
        tested = round(100.0 * geom.intersection(other).area / other.area, 2) if other.area else 0.0
    else:
        raise ValueError(f"unknown geometry measure {measure}")
    threshold, miss = _resolve_value(spec["value"], facts, tables)
    if threshold is UNKNOWN:
        return _unknown(miss or "value")
    out = _compare(tested, spec.get("op", ">="), threshold)
    out.detail = {"measure": measure}
    return out


def ev_composite(spec: dict, facts: FactSet, tables: TableResolver) -> Outcome:
    results = [evaluate_spec(p, facts, tables) for p in spec["parts"]]
    statuses = [r.status for r in results]
    missing = sorted({m for r in results for m in r.missing})
    mode = spec.get("mode", "all")
    if mode == "all":
        if DOES_NOT_MEET in statuses:
            status = DOES_NOT_MEET
        elif CANNOT_TELL in statuses:
            status = CANNOT_TELL
        elif all(s in (MEETS, NOT_APPLICABLE) for s in statuses):
            status = MEETS if MEETS in statuses else NOT_APPLICABLE
        else:
            status = CANNOT_TELL
    else:  # any
        if MEETS in statuses:
            status = MEETS
        elif CANNOT_TELL in statuses:
            status = CANNOT_TELL
        elif all(s == NOT_APPLICABLE for s in statuses):
            status = NOT_APPLICABLE
        else:
            status = DOES_NOT_MEET
    return Outcome(status, missing=missing if status == CANNOT_TELL else [],
                   detail={"mode": mode, "parts": [r.to_dict() for r in results]})


EVALUATORS: dict[str, Callable[[dict, FactSet, TableResolver], Outcome]] = {
    "threshold": ev_threshold,
    "count": ev_count,
    "boolean": ev_boolean,
    "percentage-of": ev_percentage_of,
    "table-lookup": ev_table_lookup,
    "formula": ev_formula,
    "geometry": ev_geometry,
    "composite": ev_composite,
}


def evaluate_spec(spec: dict[str, Any], facts: FactSet, tables: TableResolver) -> Outcome:
    fn = EVALUATORS.get(spec["type"])
    if fn is None:
        raise ValueError(f"unknown evaluator type {spec['type']!r}")
    return fn(spec, facts, tables)


def nominal_value(spec: dict[str, Any], facts: FactSet, tables: TableResolver) -> Any:
    """The threshold a rule would apply, for direction checks on variations.
    Returns UNKNOWN when it depends on missing facts, None when not determinable."""
    t = spec.get("type")
    if t in ("threshold", "count", "percentage-of", "geometry"):
        v, miss = _resolve_value(spec.get("value"), facts, tables)
        return v
    if t == "table-lookup":
        table = tables(spec["table"])
        if table is None:
            return None
        v, missing, _ = lookup_table(table, facts)
        return v
    if t == "formula" and "value" in spec and not isinstance(spec["value"], str):
        v, _ = _resolve_value(spec["value"], facts, tables)
        return v
    return None


def apply_effect(spec: dict[str, Any], effect: dict[str, Any]) -> dict[str, Any]:
    """Return a new evaluator spec with an exception or variation effect applied."""
    if "replace_evaluator" in effect:
        return dict(effect["replace_evaluator"])
    new = dict(spec)
    for k, v in (effect.get("set") or {}).items():
        new[k] = v
    return new
