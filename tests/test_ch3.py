"""Chapter 3 (grouped dwellings) package tests: lint gate, authored test cases, Table 3A
regeneration. Same checks as Chapter 2, via chapter_checks.py."""

from __future__ import annotations

from pathlib import Path

import pytest

import chapter_checks as cc
from rcodes.core.registry import PKG_ROOT, Registry

V = "draft-2026-10-24"
CHAPTER = "ch3"
TABLE = "table-3A"
DWELLING_TYPE = "grouped_dwelling"
CH3 = PKG_ROOT / "chapters" / CHAPTER
REPORT = Path(__file__).with_name("table-3A-regeneration-report.txt")


@pytest.fixture(scope="module")
def reg() -> Registry:
    if not (CH3 / "rules").exists():
        pytest.skip("chapter 3 rules not yet authored")
    return Registry.load(roots=[], package_dirs=[PKG_ROOT / "chapters" / "ch1", CH3], strict=False)


def test_ch3_loads_without_schema_problems(reg):
    cc.check_loads(reg, V, CHAPTER)


def test_ch3_lint_has_no_errors(reg):
    cc.check_lint(reg)


def test_ch3_every_element_has_fallback(reg):
    cc.check_fallbacks(reg, V, CHAPTER)


def test_ch3_authored_cases(reg):
    cc.check_cases(reg, V, CHAPTER)


def test_table_3A_regenerates_from_rules(reg):
    cc.check_regeneration(reg, V, CHAPTER, TABLE, DWELLING_TYPE, REPORT)
