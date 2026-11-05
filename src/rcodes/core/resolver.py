"""Resolve the rules that apply to a proposal under one code version.

Steps (spec section 5.2):
  1. chapter and pathway from the operation module (Chapter 1 Table 1.1, Figure 2.1)
  2. rule set for that chapter, filtered by dwelling type, coding, region and conditions
  3. local instruments: each targeted clause is checked against the permission tables;
     a permitted variation changes the evaluator, an unpermitted one is logged as
     "not recognised" and the base rule stands
  4. effective rules with provenance
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import evaluators as ev
from .facts import UNKNOWN, FactSet
from .registry import Registry
from .rules import Rule

RECOGNISED = "recognised"
NOT_RECOGNISED = "not recognised"


@dataclass
class Variation:
    instrument_type: str
    instrument_ref: str
    clause_ref: str
    target: dict[str, Any]
    permission: dict[str, Any]
    status: str
    reason: str = ""
    direction: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "instrument": f"{self.instrument_type}:{self.instrument_ref}",
            "clause": self.clause_ref,
            "status": self.status,
            "reason": self.reason,
            "direction": self.direction,
            "permission": self.permission,
        }


@dataclass
class EffectiveRule:
    rule: Rule
    evaluator: dict[str, Any] | None
    exceptions: list[dict[str, Any]]
    variation: Variation | None = None
    excluded: bool = False
    applicability: str = "applies"  # applies | uncertain
    applicability_missing: list[str] = field(default_factory=list)


@dataclass
class Resolution:
    version: str
    chapter: str | None
    applicability: dict[str, Any]
    da: dict[str, Any]
    rules: list[EffectiveRule]
    variations: list[Variation]
    warnings: list[str]
    facts: FactSet


def resolve(registry: Registry, app: dict[str, Any], version: str,
            chapter: str | None = None, threshold: float | None = None) -> Resolution:
    facts = FactSet.from_application(app) if threshold is None else FactSet.from_application(app, threshold)
    op = registry.operation(version)
    appl = op.applicability(facts)
    chap = chapter or appl.get("chapter")
    warnings: list[str] = list(appl.get("warnings", []))
    da = op.da_required(facts, appl)
    if chap is None:
        return Resolution(version, None, appl, da, [], [], warnings + ["no chapter applies"], facts)
    pkg = registry.package(version, chap)
    if pkg is None:
        return Resolution(version, chap, appl, da, [], [],
                          warnings + [f"no package for {version}/{chap}; nothing to evaluate"], facts)

    dwelling_type = appl.get("dwelling_type")
    r_code = appl.get("r_code")
    region = facts.get("site.region")
    region = None if region is UNKNOWN else region
    tables = registry.table_resolver(version, chap)

    effective: list[EffectiveRule] = []
    for rule in pkg.iter_rules():
        if not (rule.applies_to_type(dwelling_type) and rule.applies_to_code(r_code) and rule.applies_to_region(region)):
            continue
        status, missing = _conditions(rule, facts, tables)
        if status == "excluded":
            continue
        if region is None and rule.data.get("region", "all") != "all":
            # region unknown: a Perth-and-Peel rule and its regional twin both resolve, neither for certain
            status, missing = "uncertain", sorted(set(missing) | {"site.region"})
        effective.append(EffectiveRule(rule=rule, evaluator=rule.evaluator, exceptions=list(rule.exceptions),
                                       applicability=status, applicability_missing=missing))

    variations = _apply_instruments(app, effective, op, chap, region, facts, tables, warnings)
    return Resolution(version, chap, appl, da, effective, variations, warnings, facts)


def _conditions(rule: Rule, facts: FactSet, tables) -> tuple[str, list[str]]:
    """Rule-level applicability conditions. 'applies', 'uncertain' or 'excluded'."""
    missing: list[str] = []
    for cond in rule.conditions:
        out = ev.evaluate_spec(cond, facts, tables)
        if out.status == ev.DOES_NOT_MEET:
            return "excluded", []
        if out.status == ev.CANNOT_TELL:
            missing.extend(out.missing)
    return ("uncertain" if missing else "applies"), sorted(set(missing))


def _apply_instruments(app, effective, op, chapter, region, facts, tables, warnings) -> list[Variation]:
    log: list[Variation] = []
    by_clause = {e.rule.clause: e for e in effective}
    by_element: dict[str, list[EffectiveRule]] = {}
    for e in effective:
        by_element.setdefault(e.rule.element, []).append(e)

    for inst in (app.get("site", {}).get("instruments") or []):
        itype = inst.get("type", "other")
        iref = inst.get("ref", "?")
        for clause in inst.get("clauses", []):
            for target in clause.get("targets", []):
                if target.get("chapter") != chapter:
                    continue
                targets = []
                if target.get("clause"):
                    if target["clause"] in by_clause:
                        targets = [by_clause[target["clause"]]]
                    else:
                        log.append(Variation(itype, iref, clause.get("ref", "?"), target, {}, NOT_RECOGNISED,
                                             f"no rule {target['clause']} in {chapter}"))
                        continue
                elif target.get("element"):
                    targets = by_element.get(target["element"], [])
                    if not targets:
                        log.append(Variation(itype, iref, clause.get("ref", "?"), target, {}, NOT_RECOGNISED,
                                             f"no rules for element {target['element']} in {chapter}"))
                        continue
                for eff in targets:
                    v = _apply_one(itype, iref, clause, target, eff, inst, op, chapter, region, facts, tables)
                    log.append(v)
    return log


def _apply_one(itype, iref, clause, target, eff: EffectiveRule, inst, op, chapter, region, facts, tables) -> Variation:
    rule = eff.rule
    effect = target.get("effect") or {}
    direction = _direction(eff, effect, facts, tables)
    perm = op.permission(itype, chapter, rule.element, rule.clause, direction, region)
    level = perm.get("level")
    approved = bool(target.get("wapc_approved") or inst.get("wapc_approved"))
    v = Variation(itype, iref, clause.get("ref", "?"), target, perm, NOT_RECOGNISED, direction=direction)

    if level is None:
        v.reason = f"{itype} has no variation rights in this version"
    elif level == "wapc" and not approved:
        v.reason = "requires WAPC approval; none recorded"
    elif level == "regional-lg" and region != "regional":
        v.reason = "permitted for regional local governments only" + (
            "" if region else "; site.region not supplied")
    elif perm.get("direction") and perm["direction"] != "any":
        if direction is None:
            v.reason = f"permitted only where {perm['direction']}; direction of this variation cannot be determined"
        elif direction != perm["direction"]:
            v.reason = f"permitted only where {perm['direction']}; this variation is a {direction}"
        else:
            v.status = RECOGNISED
    else:
        v.status = RECOGNISED

    if v.status == RECOGNISED:
        if effect.get("exclude"):
            eff.excluded = True
        elif eff.evaluator is not None:
            eff.evaluator = ev.apply_effect(eff.evaluator, effect)
        eff.variation = v
        if not target.get("reading_confirmed", False):
            v.reason = "applied; instrument reading not confirmed by a planner"
        else:
            v.reason = "applied"
    return v


def _direction(eff: EffectiveRule, effect: dict[str, Any], facts, tables) -> str | None:
    """'increase' or 'decrease' of the metric, or None when it cannot be determined."""
    new = (effect.get("set") or {}).get("value")
    if new is None or eff.evaluator is None or isinstance(new, dict):
        return None
    base = ev.nominal_value(eff.evaluator, facts, tables)
    if base is None or base is UNKNOWN or isinstance(base, (bool, str, dict)):
        return None
    try:
        if float(new) > float(base):
            return "increase"
        if float(new) < float(base):
            return "decrease"
        return "any"
    except (TypeError, ValueError):
        return None
