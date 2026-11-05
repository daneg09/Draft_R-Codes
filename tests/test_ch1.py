from rcodes.chapters.ch1 import operation as op
from rcodes.core.facts import FactSet


def fs(**kw):
    return FactSet(values=kw)


def test_applicability_table_1_1():
    a = op.applicability(fs(**{"proposal.dwelling_type": "single_house", "site.r_code": "R30"}))
    assert a["chapter"] == "ch2" and a["pathway"] == "deemed-exempt-or-merit"
    assert op.applicability(fs(**{"proposal.dwelling_type": "grouped_dwelling", "site.r_code": "R160"}))["chapter"] == "ch3"
    assert op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "R40"}))["chapter"] == "ch4p1"
    a = op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "R80"}))
    assert a["chapter"] == "ch4p2" and a["pathway"] == "performance"
    assert op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "MR2"}))["chapter"] == "ch4p2"
    assert op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "R-AC3"}))["chapter"] == "ch4p2"
    a = op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "R100-SL"}))
    assert a["chapter"] is None and any("neither" in r for r in a["reasons"])
    a = op.applicability(fs(**{"proposal.dwelling_type": "multiple_dwelling", "site.r_code": "R5"}))
    assert a["chapter"] is None
    a = op.applicability(fs(**{"site.r_code": "R30"}))
    assert a["chapter"] is None and a["warnings"]
    a = op.applicability(fs(**{"proposal.dwelling_type": "single_house", "site.r_code": "R99"}))
    assert a["chapter"] is None and "unknown R-coding" in a["warnings"][0]


def test_da_required_figure_2_1():
    single = {"dwelling_type": "single_house"}
    d = op.da_required(fs(**{"site.scheme_requires_da": False}), single)
    assert d["required"] is False
    d = op.da_required(fs(), single)
    assert d["required"] is None and "scheme not checked" in d["required_label"]
    d = op.da_required(fs(**{"site.scheme_requires_da": True}), single)
    assert d["required"] is True
    d = op.da_required(fs(**{"site.heritage_or_special_control": True}), single)
    assert d["required"] is True
    assert op.da_required(fs(), {"dwelling_type": "grouped_dwelling"})["required"] is True
    assert op.da_required(fs(), {"dwelling_type": "multiple_dwelling"})["required"] is True
    assert op.da_required(fs(), {"dwelling_type": None})["required"] is None


def test_consultation_table_2_4():
    rows = op.consultation(["3.3", "3.10", "1.1"], "ch2")
    titles = {r["element_title"] for r in rows}
    assert titles == {"Street setbacks", "Visual privacy"}
    assert op.consultation(["3.9"], "ch4p1")[0]["element_title"] == "Visual privacy"
    assert op.consultation(["3.9"], "ch2")[0]["element_title"] == "Solar access for adjoining sites"
    assert op.consultation(["3.3"], "ch4p2") == []


def test_permission_lpp_table_2_5A():
    # LPP may reduce C3.3.1 without WAPC, but not garages (C3.3.3)
    p = op.permission("lpp", "ch2", "3.3", "C3.3.1", "decrease", "perth-peel")
    assert p["level"] == "without-wapc" and p["table"].endswith("T2.5A")
    p = op.permission("lpp", "ch2", "3.3", "C3.3.1", "increase", "perth-peel")
    assert p["level"] == "without-wapc" and p["direction"] == "decrease"  # best candidate returned; caller rejects
    p = op.permission("lpp", "ch2", "3.3", "C3.3.3", "decrease", "perth-peel")
    assert p["level"] == "wapc"
    # trees and landscaping: regional LGs only
    assert op.permission("lpp", "ch2", "1.2", "C1.2.1", None, "regional")["level"] == "regional-lg"
    assert op.permission("lpp", "ch2", "1.2", "C1.2.1", None, "perth-peel")["level"] == "regional-lg"
    # parking C2.3.1: regional any direction; metro only when reducing
    assert op.permission("lpp", "ch2", "2.3", "C2.3.1", "increase", "regional")["level"] == "regional-lg"
    assert op.permission("lpp", "ch2", "2.3", "C2.3.1", "decrease", "perth-peel")["level"] == "without-wapc"
    # element with no row at all falls to the table default
    p = op.permission("lpp", "ch2", "9.9", "C9.9.1", None, None)
    assert p["level"] == "wapc" and "default" in (p.get("note") or "")
    # chapter-specific element numbering: ch4p1 visual privacy is 3.9
    assert op.permission("lpp", "ch4p1", "3.9", "C3.9.1", "decrease", None)["level"] == "without-wapc"
    assert op.permission("lpp", "ch2", "3.9", "C3.9.1", "increase", None)["level"] == "without-wapc"  # solar access


def test_permission_ldp_table_2_5B():
    assert op.permission("ldp", "ch2", "3.3", "C3.3.3", "decrease", None)["level"] == "without-wapc"
    assert op.permission("ldp", "ch2", "3.3", "C3.3.3", "increase", None)["level"] == "without-wapc"
    assert op.permission("ldp", "ch2", "1.1", "C1.1.1", None, None)["level"] == "wapc"
    assert op.permission("ldp", "ch2", "3.2", "C3.2.1", "increase", None)["level"] == "wapc"
    assert op.permission("ldp", "ch2", "3.7", "C3.7.1", None, None)["level"] == "without-wapc"
    assert op.permission("ldp", "ch2", "3.7", "C3.7.5", None, None)["level"] == "wapc"


def test_permission_ch4p2_table_3_5A_and_untabled():
    assert op.permission("lpp", "ch4p2", "2.5", "A2.5.1", "increase", None)["level"] == "without-wapc"
    assert op.permission("ldp", "ch4p2", "4.8", "A4.8.1", None, None)["level"] == "wapc"
    assert op.permission("ldp", "ch4p2", "2.6", "A2.6.1", None, None)["level"] == "wapc"  # not listed: default
    assert op.permission("scheme", "ch2", "3.1", "C3.1.1", None, None)["level"] == "untabled"
    # clause 2.5.2 sits in Chapter 1A (Chapters 2, 3, 4 Part 1); Chapter 1B gives schemes and precinct
    # structure plans no untabled right over Chapter 4 Part 2 (pages 11 and 15, verified 2026-11-02)
    assert op.permission("precinct_structure_plan", "ch4p2", "2.2", "A2.2.1", None, None)["level"] is None
    assert op.permission("precinct_structure_plan", "ch2", "3.1", "C3.1.1", None, None)["level"] == "untabled"
    assert op.permission("structure_plan", "ch2", "3.1", "C3.1.1", None, None)["level"] is None
    assert op.permission("lpp", "partB", "3.1", "C3.1.1", None, None)["level"] is None
