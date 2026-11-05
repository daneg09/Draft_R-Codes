from pathlib import Path

import pytest

from rcodes.core.registry import PKG_ROOT, Registry

FIXTURES = Path(__file__).parent / "fixtures"
CH1 = PKG_ROOT / "chapters" / "ch1"


@pytest.fixture(scope="session")
def registry() -> Registry:
    """Chapter 1 (real) plus the ch2 fixture package. Default roots are not scanned so a
    real ch2 package, once it exists, does not clash with the fixture."""
    return Registry.load(roots=[], package_dirs=[CH1, FIXTURES / "pkg-ch2"])


@pytest.fixture
def app_r30() -> dict:
    return {
        "site": {"r_code": "R30", "area_m2": 375, "region": "regional",
                 "verge": {"path_or_road_offset_m": 0.5, "basis": "existing"}},
        "proposal": {"dwelling_type": "single_house"},
        "building": {"roofed_area_m2": 240},
        "parking": {"garage": {"setback_primary_m": 5.0, "parallel_parking": False, "parallel_wall_openings": 0}},
        "facts_meta": {"parking.garage.setback_primary_m": {"method": "stated", "confidence": 0.95}},
    }
