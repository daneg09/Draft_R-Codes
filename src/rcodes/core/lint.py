"""Lint rules over the loaded packages (spec section 11).

  schema      every rule, fallback and table file validates (collected at load time)
  ids         ids parse, are unique, and match the file's version and chapter
  fallback    every C or A rule has a fallback that exists
  tests       every testable rule has at least one test case naming it
  replaces    every draft rule has a replaces entry (relation new is fine)
  tables      every table-lookup references a table that exists in the version
  inputs      every fact named in an evaluator is listed in inputs
  pairing     identical ch2/ch3 rules: same evaluator, inputs, exceptions; reports drift
  judgment    judgment rules carry no evaluator
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterator

from .ids import ClauseId, is_valid
from .registry import Registry

ERROR = "error"
WARN = "warn"


@dataclass
class Finding:
    level: str
    check: str
    message: str
    rule_id: str | None = None

    def __str__(self) -> str:
        where = f" [{self.rule_id}]" if self.rule_id else ""
        return f"{self.level.upper():5} {self.check:9}{where} {self.message}"


def lint(registry: Registry, pairing: tuple[str, str] = ("ch2", "ch3")) -> list[Finding]:
    out: list[Finding] = []
    for msg in registry.problems():
        out.append(Finding(ERROR, "schema", msg))
    out.extend(_ids(registry))
    out.extend(_fallbacks(registry))
    out.extend(_tests(registry))
    out.extend(_replaces(registry))
    out.extend(_tables(registry))
    out.extend(_inputs(registry))
    out.extend(_judgment(registry))
    out.extend(_pairing(registry, *pairing))
    return out


def _ids(reg: Registry) -> Iterator[Finding]:
    seen: dict[str, str] = {}
    for pkg in reg.packages.values():
        for r in list(pkg.rules.values()) + list(pkg.fallbacks.values()):
            if not is_valid(r.id):
                yield Finding(ERROR, "ids", "id does not parse", r.id)
                continue
            cid = ClauseId.parse(r.id)
            if cid.version != r.version or cid.chapter != r.chapter:
                yield Finding(ERROR, "ids", f"id disagrees with version/chapter fields ({r.version}/{r.chapter})", r.id)
            if cid.element and r.element != "operation" and cid.element != r.element:
                yield Finding(ERROR, "ids", f"id element {cid.element} disagrees with element field {r.element}", r.id)
            if r.id in seen:
                yield Finding(ERROR, "ids", f"duplicate id (also in {seen[r.id]})", r.id)
            seen[r.id] = str(r.path)


def _fallbacks(reg: Registry) -> Iterator[Finding]:
    for r in reg.all_rules():
        if r.column in ("C", "A"):
            if not r.fallback:
                yield Finding(ERROR, "fallback", "C/A rule has no fallback", r.id)
            elif reg.rule(r.fallback) is None:
                yield Finding(ERROR, "fallback", f"fallback {r.fallback} not found", r.id)


def _tests(reg: Registry) -> Iterator[Finding]:
    covered: set[str] = set()
    for pkg in reg.packages.values():
        for case in pkg.cases:
            for rid in _case_rule_ids(case):
                covered.add(rid)
    for r in reg.all_rules():
        if r.testable and r.id not in covered:
            yield Finding(WARN, "tests", "no test case names this rule", r.id)


def _case_rule_ids(case: dict[str, Any]) -> list[str]:
    exp = case.get("expect") or {}
    ids = list(exp.get("rules", {}).keys()) if isinstance(exp.get("rules"), dict) else []
    ids += case.get("covers", [])
    return ids


def _replaces(reg: Registry) -> Iterator[Finding]:
    for r in reg.all_rules():
        v = reg.versions.get(r.version, {})
        if v.get("status") == "draft" and not r.data.get("replaces"):
            yield Finding(WARN, "replaces", "draft rule has no replaces entry (use relation 'new' if new)", r.id)


def _tables(reg: Registry) -> Iterator[Finding]:
    for r in reg.all_rules():
        resolve = reg.table_resolver(r.version, r.chapter)
        for spec in _specs(r.data):
            if spec.get("type") == "table-lookup" and resolve(spec["table"]) is None:
                yield Finding(ERROR, "tables", f"table {spec['table']} not found", r.id)


def _inputs(reg: Registry) -> Iterator[Finding]:
    for r in reg.all_rules():
        if not r.testable:
            continue
        declared = set(r.inputs)
        used = set()
        for spec in _specs(r.data):
            used |= _facts_in(spec)
        for name in sorted(used - declared):
            yield Finding(WARN, "inputs", f"fact {name} used but not listed in inputs", r.id)


def _judgment(reg: Registry) -> Iterator[Finding]:
    for r in reg.all_rules():
        if r.kind == "judgment" and r.evaluator:
            yield Finding(ERROR, "judgment", "judgment rule must not carry an evaluator", r.id)


def _pairing(reg: Registry, a: str, b: str) -> Iterator[Finding]:
    for version in reg.versions:
        pa, pb = reg.package(version, a), reg.package(version, b)
        if not pa or not pb:
            continue
        for ra in pa.rules.values():
            rb = pb.rules.get(ra.id.replace(f"/{a}/", f"/{b}/"))
            if rb is None:
                continue
            ka, kb = _signature(ra.data), _signature(rb.data)
            if ka != kb and not (ra.data.get("notes", "").startswith("diverges:") or rb.data.get("notes", "").startswith("diverges:")):
                yield Finding(WARN, "pairing", f"{a}/{b} twin rules differ; mark notes 'diverges: <why>' if intended", ra.id)


def _signature(d: dict[str, Any]) -> str:
    return json.dumps({k: d.get(k) for k in ("evaluator", "inputs", "exceptions", "conditions", "coding", "kind")},
                      sort_keys=True)


def _specs(d: dict[str, Any]) -> Iterator[dict[str, Any]]:
    if d.get("evaluator"):
        yield from _walk_spec(d["evaluator"])
    for c in d.get("conditions") or []:
        yield from _walk_spec(c)
    for e in d.get("exceptions") or []:
        yield from _walk_spec(e["condition"])
        eff = e.get("effect") or {}
        if "replace_evaluator" in eff:
            yield from _walk_spec(eff["replace_evaluator"])


def _walk_spec(spec: dict[str, Any]) -> Iterator[dict[str, Any]]:
    yield spec
    for p in spec.get("parts") or []:
        yield from _walk_spec(p)


def _facts_in(spec: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for k in ("fact", "of", "geometry", "other"):
        if spec.get(k):
            names.add(spec[k])
    v = spec.get("value")
    if isinstance(v, dict) and "fact" in v:
        names.add(v["fact"])
    if spec.get("type") == "formula":
        import ast
        from .evaluators import rewrite_dotted
        try:
            tree = ast.parse(rewrite_dotted(spec["expr"]), mode="eval")
            for n in ast.walk(tree):
                if isinstance(n, ast.Name) and n.id not in ("min", "max", "abs", "round"):
                    names.add(n.id.replace("__DOT__", "."))
        except SyntaxError:
            pass
    return names
