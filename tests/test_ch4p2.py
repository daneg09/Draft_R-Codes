"""Chapter 4 Part 2 (apartments R80 and above, performance-based) package tests: lint gate,
O fallback records, authored test cases, Table 2.1 regeneration. Same checks as Chapters 2,
3 and 4 Part 1 via chapter_checks.py, with this chapter's own metric map: Acceptable
Outcomes (column A) are the testable rules, Objectives (O) the fallbacks, and every case's
pathway is performance-assessment."""

from __future__ import annotations

from pathlib import Path

import pytest

import chapter_checks as cc
from rcodes.core.registry import PKG_ROOT, Registry

V = "draft-2026-10-24"
CHAPTER = "ch4p2"
TABLE = "table-2.1"
DWELLING_TYPE = "multiple_dwelling"
CODES = ["R80", "LR1", "R100", "R160", "MR1", "MR2", "HR1", "HR2", "HR3", "R-PA"]
CH4P2 = PKG_ROOT / "chapters" / CHAPTER
REPORT = Path(__file__).with_name("table-2.1-regeneration-report.txt")


def _metric(element: str, fact: str, op: str, probe: dict) -> dict:
    return {"element": element, "facts": {fact}, "ops": {op}, "probe": probe}


METRICS = {
    "building_height_storeys": _metric("2.2", "building.height_storeys", "<=",
                                       {"building.height_storeys": 1}),
    "boundary_wall_storeys": _metric("2.4", "building.boundary_wall_storeys", "<=",
                                     {"building.boundary_wall_storeys": 1,
                                      "building.boundary_wall_both_sides": True,
                                      "building.boundary_wall_length_pct": 50}),
    "street_setback_m": _metric("2.3", "building.street_setback_m", ">=",
                                {"building.street_setback_m": 50, "building.ground_floor_commercial": False}),
    "side_setback_m": _metric("2.4", "building.side_setback_m", ">=", {"building.side_setback_m": 50}),
    "rear_setback_m": _metric("2.4", "building.rear_setback_m", ">=", {"building.rear_setback_m": 50}),
    "plot_ratio": _metric("2.5", "building.plot_ratio", "<=", {"building.plot_ratio": 0.1}),
}


@pytest.fixture(scope="module")
def reg() -> Registry:
    if not (CH4P2 / "rules").exists():
        pytest.skip("chapter 4 part 2 rules not yet authored")
    return Registry.load(roots=[], package_dirs=[PKG_ROOT / "chapters" / "ch1", CH4P2], strict=False)


def test_ch4p2_loads_without_schema_problems(reg):
    cc.check_loads(reg, V, CHAPTER)


def test_ch4p2_lint_has_no_errors(reg):
    cc.check_lint(reg)


def test_ch4p2_every_element_has_fallback(reg):
    cc.check_fallbacks(reg, V, CHAPTER)


def test_ch4p2_authored_cases(reg):
    cc.check_cases(reg, V, CHAPTER)


def test_table_2_1_regenerates_from_rules(reg):
    cc.check_regeneration(reg, V, CHAPTER, TABLE, DWELLING_TYPE, REPORT, codes=CODES, metrics=METRICS)
