"""R-coding bands.

Numeric codes have an order (R2 < R2.5 < ... < R160). Named codes (R100-SL, LR1, MR1,
MR2, HR1, HR2, HR3, R-PA, and the current R-AC0..R-AC4) match by name only.

Band syntax accepted in rule files:
    "R2-R35"       inclusive numeric range
    "R40+"         R40 and above (numeric)
    "R25-"         R25 and below (numeric)
    "R30"          exact
    "LR1"          exact named code
    "all"          every code
    "numeric"      every numeric code
    "named"        every named code
"""

from __future__ import annotations

import re

NUMERIC = ["R2", "R2.5", "R5", "R10", "R12.5", "R15", "R17.5", "R20", "R25", "R30", "R35",
           "R40", "R50", "R60", "R80", "R100", "R160"]
NAMED = ["R100-SL", "LR1", "MR1", "MR2", "HR1", "HR2", "HR3", "R-PA",
         "R-AC0", "R-AC1", "R-AC2", "R-AC3", "R-AC4", "LR", "MR", "HR"]

_ORDER = {c: i for i, c in enumerate(NUMERIC)}


def normalise(code: str) -> str:
    c = code.strip().upper().replace(" ", "")
    c = re.sub(r"^R(\d)", r"R\1", c)
    if c in ("R100SL",):
        return "R100-SL"
    if c.startswith("RAC"):
        return "R-AC" + c[3:]
    if c == "RPA":
        return "R-PA"
    return c


def is_numeric(code: str) -> bool:
    return normalise(code) in _ORDER


def is_known(code: str) -> bool:
    c = normalise(code)
    return c in _ORDER or c in NAMED


def in_band(code: str, band: str) -> bool:
    c = normalise(code)
    b = band.strip()
    bl = b.lower()
    if bl == "all":
        return True
    if bl == "numeric":
        return c in _ORDER
    if bl == "named":
        return c in NAMED
    if b.endswith("+"):
        lo = normalise(b[:-1])
        return c in _ORDER and lo in _ORDER and _ORDER[c] >= _ORDER[lo]
    if b.endswith("-") and "-" not in b[:-1]:
        hi = normalise(b[:-1])
        return c in _ORDER and hi in _ORDER and _ORDER[c] <= _ORDER[hi]
    if "-" in b and not b.upper().startswith(("R-", "R100-SL")):
        lo, hi = (normalise(x) for x in b.split("-", 1))
        if lo in _ORDER and hi in _ORDER:
            return c in _ORDER and _ORDER[lo] <= _ORDER[c] <= _ORDER[hi]
    return c == normalise(b)


def matches(code: str, bands: list[str] | str | None) -> bool:
    """True when code falls in any band. An empty or missing band list means all."""
    if not bands:
        return True
    if isinstance(bands, str):
        bands = [bands]
    return any(in_band(code, b) for b in bands)


def compare(a: str, b: str) -> int | None:
    """-1, 0, 1 for numeric codes; None if either is named."""
    a, b = normalise(a), normalise(b)
    if a not in _ORDER or b not in _ORDER:
        return None
    return (_ORDER[a] > _ORDER[b]) - (_ORDER[a] < _ORDER[b])
