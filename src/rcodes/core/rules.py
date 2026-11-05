"""Rule records and chapter packages.

A chapter package is a directory with:
    meta.json          chapter, version, title, dwelling types, coding, summary table
    rules/**/*.json    one rule record per file (schema: rule)
    fallbacks/*.json   M / O / DG records (schema: rule, column M|O|DG, kind judgment)
    tables/*.json      lookup tables (schema: table)
    graph/*.jsonld     relationship edges (optional)
    tests/cases/*.json test cases (optional)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from . import codings
from .ids import ClauseId
from .schema import validate


@dataclass
class Rule:
    data: dict[str, Any]
    path: Path | None = None

    # convenience accessors -------------------------------------------------
    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def cid(self) -> ClauseId:
        return ClauseId.parse(self.id)

    @property
    def version(self) -> str:
        return self.data["version"]

    @property
    def chapter(self) -> str:
        return self.data["chapter"]

    @property
    def element(self) -> str:
        return self.data["element"]

    @property
    def clause(self) -> str:
        return self.cid.clause

    @property
    def kind(self) -> str:
        return self.data["kind"]

    @property
    def column(self) -> str:
        return self.data["column"]

    @property
    def testable(self) -> bool:
        return self.kind in ("measurable", "conditional") and self.column in ("C", "A", "operation", "table")

    @property
    def evaluator(self) -> dict[str, Any] | None:
        return self.data.get("evaluator")

    @property
    def exceptions(self) -> list[dict[str, Any]]:
        return self.data.get("exceptions") or []

    @property
    def conditions(self) -> list[dict[str, Any]]:
        return self.data.get("conditions") or []

    @property
    def fallback(self) -> str | None:
        return self.data.get("fallback")

    @property
    def inputs(self) -> list[str]:
        return self.data.get("inputs") or []

    def applies_to_type(self, dwelling_type: str | None) -> bool:
        kinds = self.data.get("applies_to") or ["any"]
        return "any" in kinds or dwelling_type is None or dwelling_type in kinds

    def applies_to_code(self, r_code: str | None) -> bool:
        if r_code is None:
            return True
        return codings.matches(r_code, self.data.get("coding"))

    def applies_to_region(self, region: str | None) -> bool:
        want = self.data.get("region", "all")
        return want == "all" or region is None or want == region


@dataclass
class ChapterPackage:
    root: Path
    meta: dict[str, Any]
    rules: dict[str, Rule] = field(default_factory=dict)
    fallbacks: dict[str, Rule] = field(default_factory=dict)
    tables: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[dict[str, Any]] = field(default_factory=list)
    cases: list[dict[str, Any]] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def chapter(self) -> str:
        return self.meta["chapter"]

    @property
    def version(self) -> str:
        return self.meta["version"]

    @classmethod
    def load(cls, root: Path, strict: bool = True) -> "ChapterPackage":
        meta = _read_json(root / "meta.json")
        pkg = cls(root=root, meta=meta)
        for p in sorted((root / "rules").rglob("*.json")) if (root / "rules").exists() else []:
            doc = _read_json(p)
            errs = validate("rule", doc)
            if errs:
                pkg.problems.append(f"{p}: " + "; ".join(errs))
                if strict:
                    continue
            pkg.rules[doc["id"]] = Rule(doc, p)
        for p in sorted((root / "fallbacks").rglob("*.json")) if (root / "fallbacks").exists() else []:
            doc = _read_json(p)
            errs = validate("rule", doc)
            if errs:
                pkg.problems.append(f"{p}: " + "; ".join(errs))
                if strict:
                    continue
            pkg.fallbacks[doc["id"]] = Rule(doc, p)
        for p in sorted((root / "tables").glob("*.json")) if (root / "tables").exists() else []:
            doc = _read_json(p)
            errs = validate("table", doc)
            if errs:
                pkg.problems.append(f"{p}: " + "; ".join(errs))
                if strict:
                    continue
            pkg.tables[doc["id"]] = doc
            pkg.tables.setdefault(p.stem, doc)
        for p in sorted((root / "graph").glob("*.jsonld")) if (root / "graph").exists() else []:
            doc = _read_json(p)
            graph = doc.get("@graph", doc if isinstance(doc, list) else [])
            pkg.edges.extend(graph)
        for p in sorted((root / "tests" / "cases").glob("*.json")) if (root / "tests" / "cases").exists() else []:
            doc = _read_json(p)
            for case in (doc if isinstance(doc, list) else [doc]):
                case.setdefault("_path", str(p))
                pkg.cases.append(case)
        return pkg

    def table(self, ref: str) -> dict[str, Any] | None:
        return self.tables.get(ref)

    def iter_rules(self) -> Iterator[Rule]:
        return iter(self.rules.values())

    def rules_for_element(self, element: str) -> list[Rule]:
        return [r for r in self.rules.values() if r.element == element]


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
