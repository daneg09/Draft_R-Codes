"""Evaluate resolved rules and build a run result.

Exception semantics (spec 6.1): exceptions are tried in the order listed. The first
exception whose condition MEETS replaces or adjusts the evaluator. If the base test
DOES_NOT_MEET and some exception's condition is CANNOT_TELL, the outcome is CANNOT_TELL
with that exception's missing facts listed, because the exception might rescue it.
If the base test MEETS, exceptions are not needed and the outcome stands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import evaluators as ev
from .facts import FactSet
from .registry import Registry
from .resolver import EffectiveRule, Resolution, resolve

PATHWAY_DEEMED_EXEMPT = "deemed-exempt"
PATHWAY_MERIT = "merit-assessment"
PATHWAY_PERFORMANCE = "performance-assessment"
PATHWAY_UNDETERMINED = "undetermined"


@dataclass
class RuleResult:
    rule_id: str
    chapter: str
    element: str
    element_title: str
    title: str
    column: str
    kind: str
    status: str
    outcome: dict[str, Any] = field(default_factory=dict)
    exception_used: str | None = None
    fallback: str | None = None
    variation: dict[str, Any] | None = None
    applicability: str = "applies"
    missing: list[str] = field(default_factory=list)
    source: dict[str, Any] = field(default_factory=dict)
    verify: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = {k: v for k, v in self.__dict__.items() if v not in (None, "", [], {}, False)}
        d["status"] = self.status
        return d


@dataclass
class RunResult:
    version: str
    chapter: str | None
    applicability: dict[str, Any]
    da: dict[str, Any]
    pathway: str
    results: list[RuleResult]
    elements_on_merit: list[str]
    consultation: list[dict[str, Any]]
    variations: list[dict[str, Any]]
    missing: dict[str, list[str]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "chapter": self.chapter,
            "applicability": self.applicability,
            "development_application": self.da,
            "pathway": self.pathway,
            "elements_on_merit": self.elements_on_merit,
            "consultation": self.consultation,
            "results": [r.to_dict() for r in self.results],
            "variations": self.variations,
            "missing": self.missing,
            "warnings": self.warnings,
            "counts": self.counts(),
        }

    def counts(self) -> dict[str, int]:
        c: dict[str, int] = {}
        for r in self.results:
            c[r.status] = c.get(r.status, 0) + 1
        return c


def evaluate_rule(eff: EffectiveRule, facts: FactSet, tables) -> RuleResult:
    rule = eff.rule
    base = RuleResult(
        rule_id=rule.id, chapter=rule.chapter, element=rule.element,
        element_title=rule.data.get("element_title", ""), title=rule.data.get("title", ""),
        column=rule.column, kind=rule.kind, status=ev.NOT_EVALUATED,
        fallback=rule.fallback, source=rule.data.get("source", {}), verify=bool(rule.data.get("verify")),
        notes=rule.data.get("notes", ""), applicability=eff.applicability,
        variation=eff.variation.to_dict() if eff.variation else None,
    )
    if eff.excluded:
        base.status = ev.NOT_APPLICABLE
        base.outcome = {"reason": "excluded by local instrument"}
        return base
    if not rule.testable or eff.evaluator is None:
        base.status = ev.NOT_EVALUATED
        base.outcome = {"reason": "judgment provision; not evaluated"}
        return base

    out = ev.evaluate_spec(eff.evaluator, facts, tables)
    exception_used = None
    if out.status != ev.MEETS and eff.exceptions:
        pending_missing: list[str] = []
        for exc in eff.exceptions:
            cond = ev.evaluate_spec(exc["condition"], facts, tables)
            if cond.status == ev.MEETS:
                if (exc.get("effect") or {}).get("not_applicable"):
                    out = ev.Outcome(ev.NOT_APPLICABLE, detail={"exception": exc["label"]})
                else:
                    out = ev.evaluate_spec(ev.apply_effect(eff.evaluator, exc["effect"]), facts, tables)
                exception_used = exc["label"]
                if out.status == ev.MEETS:
                    break
            elif cond.status == ev.CANNOT_TELL:
                pending_missing.extend(cond.missing)
        if out.status in (ev.DOES_NOT_MEET, ev.CANNOT_TELL) and pending_missing:
            out = ev.Outcome(ev.CANNOT_TELL, tested=out.tested, threshold=out.threshold, op=out.op,
                             missing=sorted(set(out.missing + pending_missing)),
                             detail={"reason": "an exception may apply; its facts are missing"})
    base.status = out.status
    base.outcome = out.to_dict()
    base.exception_used = exception_used
    base.missing = list(out.missing)
    if eff.applicability == "uncertain" and eff.applicability_missing:
        if base.status in (ev.MEETS, ev.DOES_NOT_MEET, ev.CANNOT_TELL):
            base.missing = sorted(set(base.missing + eff.applicability_missing))
        if base.status in (ev.MEETS, ev.DOES_NOT_MEET, ev.CANNOT_TELL, ev.NOT_APPLICABLE):
            base.notes = (base.notes + " " if base.notes else "") + "applicability uncertain: " + ", ".join(eff.applicability_missing)
    return base


def run(registry: Registry, app: dict[str, Any], version: str, chapter: str | None = None,
        threshold: float | None = None) -> RunResult:
    res = resolve(registry, app, version, chapter, threshold)
    op = registry.operation(version)
    tables = registry.table_resolver(version, res.chapter or "")
    results = [evaluate_rule(e, res.facts, tables) for e in res.rules]
    pathway, on_merit = _pathway(registry, res, results)
    consultation = op.consultation(on_merit, res.chapter) if on_merit and res.chapter else []
    return RunResult(
        version=version, chapter=res.chapter, applicability=res.applicability, da=res.da,
        pathway=pathway, results=results, elements_on_merit=on_merit, consultation=consultation,
        variations=[v.to_dict() for v in res.variations], missing=group_missing(results),
        warnings=list(res.warnings),
    )


def _pathway(registry: Registry, res: Resolution, results: list[RuleResult]) -> tuple[str, list[str]]:
    if res.chapter is None:
        return PATHWAY_UNDETERMINED, []
    pkg = registry.package(res.version, res.chapter)
    kind = (pkg.meta.get("pathway") if pkg else None) or "deemed-exempt-or-merit"
    tested = [r for r in results if r.column in ("C", "A")]
    failing = sorted({r.element for r in tested if r.status == ev.DOES_NOT_MEET})
    unknown = sorted({r.element for r in tested if r.status == ev.CANNOT_TELL})
    if kind == "performance":
        return PATHWAY_PERFORMANCE, failing
    if failing:
        return PATHWAY_MERIT, failing
    if unknown:
        return PATHWAY_UNDETERMINED, []
    if not tested:
        return PATHWAY_UNDETERMINED, []
    return PATHWAY_DEEMED_EXEMPT, []


SOURCE_HINTS = [
    ("site.verge", "civil design / subdivision engineering drawings"),
    ("site.instruments", "local planning instrument"),
    ("site.", "lot plan / certificate of title / scheme map"),
    ("adjoining.", "adjoining lot information: scheme map, survey, neighbour's approved plans"),
    ("overshadow.", "shadow diagram, midday 21 June"),
    ("privacy.", "elevations and site plan: cone of vision"),
    ("site_works.", "site works plan: levels, retaining"),
    ("outbuilding.", "site plan: outbuildings"),
    ("subdivision.", "subdivision plan or title"),
    ("ancillary.", "floor plan: ancillary dwelling"),
    ("proposal.", "application form"),
    ("building.", "site plan and elevations"),
    ("dwellings.", "floor plans"),
    ("landscape.", "landscape plan"),
    ("parking.", "site plan"),
    ("services.", "site plan"),
    ("drawings.", "drawings (IFC / GeoJSON)"),
]


def group_missing(results: list[RuleResult]) -> dict[str, list[str]]:
    out: dict[str, set[str]] = {}
    for r in results:
        for m in r.missing:
            name = m.split(":")[0]
            src = next((s for prefix, s in SOURCE_HINTS if name.startswith(prefix)), "unknown source")
            out.setdefault(src, set()).add(name)
    return {k: sorted(v) for k, v in sorted(out.items())}


def compare(registry: Registry, app: dict[str, Any], versions: list[str]) -> dict[str, Any]:
    """Run several versions and pair results through `replaces` edges."""
    runs = {v: run(registry, app, v) for v in versions}
    pairs: list[dict[str, Any]] = []
    by_id = {v: {r.rule_id: r for r in rr.results} for v, rr in runs.items()}
    seen: set[tuple[str, str]] = set()
    for v, rr in runs.items():
        for r in rr.results:
            rule = registry.rule(r.rule_id)
            for rep in (rule.data.get("replaces") if rule else None) or []:
                old = rep.get("id")
                if old is None:
                    pairs.append({"new": r.to_dict(), "old": None, "relation": rep["relation"]})
                    continue
                matched = False
                for ov, res in by_id.items():
                    if old in res and (old, r.rule_id) not in seen:
                        seen.add((old, r.rule_id))
                        matched = True
                        pairs.append({"new": r.to_dict(), "old": res[old].to_dict(), "relation": rep["relation"],
                                      "changed": res[old].status != r.status})
                if not matched and (old, r.rule_id) not in seen:
                    seen.add((old, r.rule_id))
                    pairs.append({"new": r.to_dict(), "old": None, "old_id": old, "relation": rep["relation"],
                                  "note": "replaced rule not loaded in any run"})
    return {"runs": {v: rr.to_dict() for v, rr in runs.items()}, "pairs": pairs}
