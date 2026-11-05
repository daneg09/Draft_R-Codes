import pytest

from rcodes.core import codings
from rcodes.core.facts import UNKNOWN, FactSet
from rcodes.core.ids import ClauseId, is_valid, make


def test_id_roundtrip():
    cid = ClauseId.parse("rcodes:draft-2026-10-24/ch2/C3.3.3#table-3.3c")
    assert cid.version == "draft-2026-10-24" and cid.chapter == "ch2" and cid.clause == "C3.3.3"
    assert cid.fragment == "table-3.3c" and cid.element == "3.3" and cid.column == "C"
    assert str(cid) == "rcodes:draft-2026-10-24/ch2/C3.3.3#table-3.3c"
    assert make("vol1-v3-2026-04-10", "partB", "5.2.1-C1.1") == "rcodes:vol1-v3-2026-04-10/partB/5.2.1-C1.1"
    assert ClauseId.parse("rcodes:draft-2026-10-24/ch4p2/A2.5.1").column == "A"
    assert ClauseId.parse("rcodes:draft-2026-10-24/ch4p2/DG2.2.1").column == "DG"


def test_id_invalid():
    assert not is_valid("ch2/C3.3.3")
    with pytest.raises(ValueError):
        ClauseId.parse("nope")


@pytest.mark.parametrize("code,band,expected", [
    ("R30", "R2-R35", True), ("R40", "R2-R35", False), ("R2", "R2-R35", True), ("R35", "R2-R35", True),
    ("R40", "R40+", True), ("R35", "R40+", False), ("R160", "R40+", True),
    ("R25", "R25-", True), ("R30", "R25-", False),
    ("R30", "R30", True), ("r 30", "R30", True),
    ("LR1", "LR1", True), ("LR1", "R2-R35", False), ("LR1", "named", True), ("R30", "named", False),
    ("R100-SL", "R100-SL", True), ("R100-SL", "R40+", False), ("R100", "all", True),
])
def test_bands(code, band, expected):
    assert codings.in_band(code, band) is expected


def test_matches_and_compare():
    assert codings.matches("R30", ["R2-R25", "R30-R35"])
    assert codings.matches("R30", None)
    assert codings.compare("R30", "R40") == -1 and codings.compare("R40", "R40") == 0
    assert codings.compare("LR1", "R40") is None
    assert codings.is_known("R-AC4") and codings.normalise("RAC4") == "R-AC4"


def test_factset_flatten_and_unknown():
    doc = {
        "site": {"r_code": "R30", "area_m2": None, "verge": {"path_or_road_offset_m": 1.2}},
        "dwellings": [{"bedrooms": 3}, {"bedrooms": 2}],
        "facts_meta": {"site.verge.path_or_road_offset_m": {"method": "inferred", "confidence": 0.4}},
    }
    fs = FactSet.from_application(doc)
    assert fs.get("site.r_code") == "R30"
    assert fs.get("site.area_m2") is UNKNOWN
    assert fs.get("site.verge.path_or_road_offset_m") is UNKNOWN  # below threshold
    assert fs.get("dwellings.count") == 2 and fs.get("dwellings.1.bedrooms") == 2
    assert fs.get("nothing.here") is UNKNOWN
    assert any("confidence 0.40" in m for m in fs.missing_log)
    assert FactSet.from_application(doc, threshold=0.3).get("site.verge.path_or_road_offset_m") == 1.2
    assert not UNKNOWN
