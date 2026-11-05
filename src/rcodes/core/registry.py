"""Version registry and chapter package discovery.

versions.json lists every code version the engine knows. Chapter packages are found by
scanning rcodes/chapters/* and rcodes/current/* for meta.json. A package belongs to the
version named in its meta. An operation package (Chapter 1, Vol 1 Part A) names a Python
module in meta["operation_module"] that provides applicability, DA, consultation and
permission functions; see rcodes.chapters.ch1.operation for the interface.
"""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .rules import ChapterPackage, Rule

PKG_ROOT = Path(__file__).resolve().parent.parent
VERSIONS_FILE = Path(__file__).parent / "versions.json"


@dataclass
class Registry:
    versions: dict[str, dict[str, Any]]
    packages: dict[tuple[str, str], ChapterPackage] = field(default_factory=dict)  # (version, chapter)
    extra_roots: list[Path] = field(default_factory=list)

    @classmethod
    def load(cls, extra_roots: list[Path] | None = None, strict: bool = True,
             roots: list[Path] | None = None, package_dirs: list[Path] | None = None) -> "Registry":
        """Load versions and packages.

        roots         replaces the default roots (chapters/, current/) when given
        extra_roots   additional roots scanned after the defaults
        package_dirs  individual package directories to add (tests use this)
        """
        with VERSIONS_FILE.open(encoding="utf-8") as fh:
            versions = {v["id"]: v for v in json.load(fh)["versions"]}
        reg = cls(versions=versions, extra_roots=list(extra_roots or []))
        scan = list(roots) if roots is not None else [PKG_ROOT / "chapters", PKG_ROOT / "current"]
        scan += reg.extra_roots
        dirs: list[Path] = []
        for root in scan:
            if root.exists():
                dirs += [m.parent for m in sorted(root.glob("*/meta.json"))]
        dirs += [Path(p) for p in (package_dirs or [])]
        for d in dirs:
            pkg = ChapterPackage.load(d, strict=strict)
            key = (pkg.version, pkg.chapter)
            if key in reg.packages:
                raise ValueError(f"duplicate package {key}: {reg.packages[key].root} and {pkg.root}")
            reg.packages[key] = pkg
        return reg

    def version(self, vid: str) -> dict[str, Any]:
        if vid not in self.versions:
            raise KeyError(f"unknown code version {vid!r}; known: {sorted(self.versions)}")
        return self.versions[vid]

    def package(self, version: str, chapter: str) -> ChapterPackage | None:
        return self.packages.get((version, chapter))

    def packages_for(self, version: str) -> list[ChapterPackage]:
        return [p for (v, _), p in self.packages.items() if v == version]

    def operation(self, version: str) -> Any:
        """The operation module for a version (Chapter 1 for the draft)."""
        v = self.version(version)
        pkg = self.package(version, v["operation_chapter"])
        if pkg is None:
            raise KeyError(f"version {version} has no operation package ({v['operation_chapter']})")
        mod = pkg.meta.get("operation_module")
        if not mod:
            raise KeyError(f"operation package {pkg.root} has no operation_module in meta.json")
        return importlib.import_module(mod)

    def rule(self, rule_id: str) -> Rule | None:
        for pkg in self.packages.values():
            if rule_id in pkg.rules:
                return pkg.rules[rule_id]
            if rule_id in pkg.fallbacks:
                return pkg.fallbacks[rule_id]
        return None

    def table_resolver(self, version: str, chapter: str):
        """Tables are looked up in the chapter package first, then any package of the version."""
        pkg = self.package(version, chapter)

        def resolve(ref: str) -> dict[str, Any] | None:
            if pkg and ref in pkg.tables:
                return pkg.tables[ref]
            for other in self.packages_for(version):
                if ref in other.tables:
                    return other.tables[ref]
            return None

        return resolve

    def all_rules(self) -> list[Rule]:
        return [r for p in self.packages.values() for r in p.rules.values()]

    def all_fallbacks(self) -> list[Rule]:
        return [r for p in self.packages.values() for r in p.fallbacks.values()]

    def problems(self) -> list[str]:
        return [f"[{p.version}/{p.chapter}] {msg}" for p in self.packages.values() for msg in p.problems]

    def summary(self) -> dict[str, Any]:
        return {
            "versions": list(self.versions),
            "packages": [
                {"version": p.version, "chapter": p.chapter, "rules": len(p.rules), "fallbacks": len(p.fallbacks),
                 "tables": len(p.tables), "cases": len(p.cases), "path": str(p.root)}
                for p in self.packages.values()
            ],
        }
