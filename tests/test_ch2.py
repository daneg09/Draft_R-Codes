"""Chapter 2 package tests: lint gate, authored test cases, Table 2A regeneration.

The checks live in chapter_checks.py, shared with Chapter 3 (test_ch3.py).
"""

from __future__ import annotations

from pathlib import Path

import pytest

import chapter_checks as cc
from rcodes.core.registry import PKG_ROOT, Registry

V = "draft-2026-10-24"
CHAPTER = "ch2"
TABLE = "table-2A"
DWELLING_TYPE = "single_house"
CH2 = PKG_ROOT / "chapters" / CHAPTER
REPORT = Path(__file__).with_name("table-2A-regeneration-report.txt")


@pytest.fixture(scope="module")
def reg() -> Registry:
    if not (CH2 / "rules").exists():
        pytest.skip("chapter 2 rules not yet authored")
    return Registry.load(roots=[], package_dirs=[PKG_ROOT / "chapters" / "ch1", CH2], strict=False)


def test_ch2_loads_without_schema_problems(reg):
    cc.check_loads(reg, V, CHAPTER)


def test_ch2_lint_has_no_errors(reg):
    cc.check_lint(reg)


def test_ch2_every_element_has_fallback(reg):
    cc.check_fallbacks(reg, V, CHAPTER)


def test_ch2_authored_cases(reg):
    cc.check_cases(reg, V, CHAPTER)


def test_table_2A_regenerates_from_rules(reg):
    cc.check_regeneration(reg, V, CHAPTER, TABLE, DWELLING_TYPE, REPORT)
