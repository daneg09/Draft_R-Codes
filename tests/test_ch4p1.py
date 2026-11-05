"""Chapter 4 Part 1 (apartments R10 to R60) package tests: lint gate, authored test cases,
Table 4A regeneration. Same checks as Chapters 2 and 3, via chapter_checks.py, probing only
the codings the chapter covers."""

from __future__ import annotations

from pathlib import Path

import pytest

import chapter_checks as cc
from rcodes.core.registry import PKG_ROOT, Registry

V = "draft-2026-10-24"
CHAPTER = "ch4p1"
TABLE = "table-4A"
DWELLING_TYPE = "multiple_dwelling"
CODES = ["R10", "R12.5", "R15", "R17.5", "R20", "R25", "R30", "R35", "R40", "R50", "R60"]
CH4P1 = PKG_ROOT / "chapters" / CHAPTER
REPORT = Path(__file__).with_name("table-4A-regeneration-report.txt")


@pytest.fixture(scope="module")
def reg() -> Registry:
    if not (CH4P1 / "rules").exists():
        pytest.skip("chapter 4 part 1 rules not yet authored")
    return Registry.load(roots=[], package_dirs=[PKG_ROOT / "chapters" / "ch1", CH4P1], strict=False)


def test_ch4p1_loads_without_schema_problems(reg):
    cc.check_loads(reg, V, CHAPTER)


def test_ch4p1_lint_has_no_errors(reg):
    cc.check_lint(reg)


def test_ch4p1_every_element_has_fallback(reg):
    cc.check_fallbacks(reg, V, CHAPTER)


def test_ch4p1_authored_cases(reg):
    cc.check_cases(reg, V, CHAPTER)


def test_table_4A_regenerates_from_rules(reg):
    cc.check_regeneration(reg, V, CHAPTER, TABLE, DWELLING_TYPE, REPORT, codes=CODES)
