"""Command line: python -m rcodes <command>

  run <app.json> --version V [--chapter C] [--md]     check one proposal
  compare <app.json> --versions V1 V2                 run several versions, pair by replaces
  applicability <app.json> --version V                chapter, pathway and DA only
  lint                                                lint all packages
  rules [--version V] [--chapter C]                   markdown table of rules
  summary                                             packages loaded
  publish [--out edition]                             generate the recall layers of the edition
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import evaluate, lint as lint_mod, report
from .core.facts import FactSet
from .core.registry import Registry


def _load_app(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str] | None = None) -> int:
    head = (argv if argv is not None else sys.argv[1:])[:1]
    rest = (argv if argv is not None else sys.argv[1:])[1:]
    if head == ["export-jsonld"]:
        from .core import export_jsonld
        return export_jsonld.main(rest)
    if head == ["export-schema"]:
        from .core import export_schema
        return export_schema.main(rest)
    p = argparse.ArgumentParser(prog="rcodes", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("run")
    s.add_argument("app")
    s.add_argument("--version", default="draft-2026-10-24")
    s.add_argument("--chapter")
    s.add_argument("--md", action="store_true", help="markdown instead of JSON")
    s.add_argument("--threshold", type=float, default=None, help="confidence threshold (default 0.8)")

    s = sub.add_parser("compare")
    s.add_argument("app")
    s.add_argument("--versions", nargs="+", required=True)

    s = sub.add_parser("applicability")
    s.add_argument("app")
    s.add_argument("--version", default="draft-2026-10-24")

    sub.add_parser("lint")

    s = sub.add_parser("rules")
    s.add_argument("--version")
    s.add_argument("--chapter")

    sub.add_parser("summary")

    s = sub.add_parser("publish")
    s.add_argument("--out", default=None, help="output directory (default: edition/ at the repository root)")

    p.add_argument("--package-dir", action="append", default=[], metavar="DIR",
                   help="extra chapter package directory to load (repeatable; for development)")
    a = p.parse_args(argv)
    reg = Registry.load(strict=False, package_dirs=[Path(d) for d in a.package_dir])

    if a.cmd == "run":
        res = evaluate.run(reg, _load_app(a.app), a.version, a.chapter, a.threshold)
        sys.stdout.write(report.to_markdown(res) if a.md else report.to_json(res) + "\n")
        return 0
    if a.cmd == "compare":
        out = evaluate.compare(reg, _load_app(a.app), a.versions)
        json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    if a.cmd == "applicability":
        facts = FactSet.from_application(_load_app(a.app))
        op = reg.operation(a.version)
        appl = op.applicability(facts)
        json.dump({"applicability": appl, "development_application": op.da_required(facts, appl)},
                  sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    if a.cmd == "lint":
        findings = lint_mod.lint(reg)
        for f in findings:
            print(f)
        errors = sum(1 for f in findings if f.level == lint_mod.ERROR)
        print(f"{len(findings)} findings, {errors} errors")
        return 1 if errors else 0
    if a.cmd == "rules":
        rows = ["| ID | Element | Title | Kind | Column | Coding | Fallback | Verify |", "|---|---|---|---|---|---|---|---|"]
        for r in sorted(reg.all_rules(), key=lambda r: r.id):
            if a.version and r.version != a.version:
                continue
            if a.chapter and r.chapter != a.chapter:
                continue
            d = r.data
            rows.append(f"| {r.id} | {d['element']} {d.get('element_title', '')} | {d['title']} | {d['kind']} | {d['column']} "
                        f"| {', '.join(d.get('coding') or [])} | {d.get('fallback') or ''} | {'yes' if d.get('verify') else ''} |")
        print("\n".join(rows))
        return 0
    if a.cmd == "publish":
        from .core import publish as publish_mod
        ed = publish_mod.publish(reg, Path(a.out) if a.out else None)
        print(publish_mod.report(ed))
        return 1 if ed.unplaced else 0
    if a.cmd == "summary":
        json.dump(reg.summary(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        for prob in reg.problems():
            print("PROBLEM", prob, file=sys.stderr)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
