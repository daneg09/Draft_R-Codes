"""Chapter 2 / Chapter 3 twin pairing.

Loads ch1 + ch2 + ch3, fails on any lint ERROR, writes the pairing WARN findings to
tests/pairing-report.txt, and makes undeclared divergence a hard failure: every ch3 rule
with a ch2 twin must either match the twin's signature or carry notes starting
"diverges:".
"""

from __future__ import annotations

from pathlib import Path

import pytest

from rcodes.core import lint
from rcodes.core.registry import PKG_ROOT, Registry

V = "draft-2026-10-24"
CHAPTERS = PKG_ROOT / "chapters"
REPORT = Path(__file__).with_name("pairing-report.txt")


@pytest.fixture(scope="module")
def reg() -> Registry:
    if not (CHAPTERS / "ch3" / "rules").exists():
        pytest.skip("chapter 3 rules not yet authored")
    return Registry.load(roots=[], package_dirs=[CHAPTERS / "ch1", CHAPTERS / "ch2", CHAPTERS / "ch3"],
                         strict=False)


def test_lint_no_errors_and_pairing_report(reg):
    findings = lint.lint(reg, pairing=("ch2", "ch3"))
    pairing = [str(f) for f in findings if f.check == "pairing" and f.level == lint.WARN]
    REPORT.write_text("\n".join([f"Pairing warnings ({len(pairing)}):"] + pairing) + "\n", encoding="utf-8", newline="\n")
    errors = [str(f) for f in findings if f.level == lint.ERROR]
    assert errors == [], "\n".join(errors)


def test_ch3_divergences_are_declared(reg):
    ch2, ch3 = reg.package(V, "ch2"), reg.package(V, "ch3")
    assert ch2 is not None and ch3 is not None, "ch2 and ch3 packages must both load"
    undeclared = []
    for r3 in ch3.rules.values():
        r2 = ch2.rules.get(r3.id.replace("/ch3/", "/ch2/"))
        if r2 is None:
            continue
        if lint._signature(r3.data) != lint._signature(r2.data) \
                and not (r3.data.get("notes") or "").startswith("diverges:"):
            undeclared.append(r3.id)
    assert undeclared == [], ("ch3 rules differ from their ch2 twin without notes 'diverges: <why>':\n"
                              + "\n".join(undeclared))
