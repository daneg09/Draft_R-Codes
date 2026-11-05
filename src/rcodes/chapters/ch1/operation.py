"""Chapter 1 operation logic. This is the interface every operation module provides:

    applicability(facts) -> dict   chapter, dwelling_type, r_code, pathway, reasons, warnings
    da_required(facts, appl) -> dict   required (True/False/None), required_label, basis
    consultation(elements, chapter) -> list[dict]
    permission(instrument_type, chapter, element, clause, direction, region) -> dict

All data comes from the JSON files in data/. Nothing here is chapter-2/3/4 specific
beyond the element numbers those chapters use.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from rcodes.core import codings
from rcodes.core.facts import UNKNOWN, FactSet

DATA = Path(__file__).parent / "data"

PERMISSION_RANK = {"untabled": 0, "without-wapc": 1, "regional-lg": 2, "wapc": 3}


@lru_cache(maxsize=None)
def _load(name: str) -> dict[str, Any]:
    with (DATA / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def _permission_tables() -> list[dict[str, Any]]:
    tables = [_load("table-2.5A.json"), _load("table-2.5B.json"), _load("table-3.5A.json")]
    c = _load("clause-2.5.2.json")
    if c.get("enabled", True):
        tables.append(c)
    return tables


# --- applicability (Table 1.1) -------------------------------------------------------

def applicability(facts: FactSet) -> dict[str, Any]:
    dwelling_type = facts.get("proposal.dwelling_type")
    r_code = facts.get("site.r_code")
    out: dict[str, Any] = {
        "chapter": None, "pathway": None,
        "dwelling_type": None if dwelling_type is UNKNOWN else dwelling_type,
        "r_code": None if r_code is UNKNOWN else codings.normalise(r_code),
        "reasons": [], "warnings": [], "source": _load("table-1.1.json")["id"],
    }
    if dwelling_type is UNKNOWN:
        out["warnings"].append("proposal.dwelling_type not supplied; no chapter can be selected")
        return out
    if r_code is UNKNOWN:
        out["warnings"].append("site.r_code not supplied; no chapter can be selected")
        return out
    if not codings.is_known(r_code):
        out["warnings"].append(f"unknown R-coding {r_code!r}")
        return out
    for row in _load("table-1.1.json")["rows"]:
        if row["dwelling_type"] != dwelling_type:
            continue
        if codings.matches(r_code, row["coding"]):
            out["chapter"] = row["chapter"]
            out["pathway"] = row["pathway"]
            out["reasons"].append(f"Table 1.1: {dwelling_type} at {out['r_code']} -> {row['chapter'] or 'no chapter'}")
            if row.get("note") and _note_applies(row, r_code):
                out["reasons"].append("Note: " + row["note"])
            if row.get("verify"):
                out["warnings"].append("Table 1.1 row not yet verified against the rendered page")
            break
    else:
        out["warnings"].append(f"Table 1.1 has no row for {dwelling_type} at {out['r_code']}")
    anc = facts.get("proposal.ancillary_dwelling")
    if anc is True:
        out["reasons"].append("Ancillary dwelling provisions (element 2.8) apply within the selected chapter")
    return out


# The single-house and grouped-dwelling rows cover "all" codings; their notes are about how
# R100, R160 and the LR/MR/HR codes are presented, so they print only for those codings.
_ALL_ROW_NOTE_CODINGS = ["R100", "R160", "R100-SL", "LR", "MR", "HR", "LR1", "MR1", "MR2", "HR1", "HR2", "HR3"]


def _note_applies(row: dict[str, Any], r_code: str) -> bool:
    if row["coding"] == ["all"]:
        return codings.matches(r_code, _ALL_ROW_NOTE_CODINGS)
    return True


# --- development application (Figure 2.1) --------------------------------------------

def da_required(facts: FactSet, appl: dict[str, Any]) -> dict[str, Any]:
    fig = _load("figure-2.1.json")
    dt = appl.get("dwelling_type")
    out: dict[str, Any] = {"required": None, "required_label": "cannot tell", "basis": fig["basis"], "source": fig["id"]}
    row = next((r for r in fig["rows"] if r["dwelling_type"] == dt), None)
    if row is None:
        out["basis"] = "dwelling type unknown; " + out["basis"]
        return out
    if row["required"]:
        out["required"] = True
        out["required_label"] = "required"
        out["basis"] = row["note"]
        return out
    scheme = facts.get("site.scheme_requires_da")
    heritage = facts.get("site.heritage_or_special_control")
    if scheme is True or heritage is True:
        out["required"] = True
        out["required_label"] = "required (scheme)"
        out["basis"] = "The local planning scheme requires development approval for this single house irrespective of the R-Codes."
    elif scheme is UNKNOWN:
        out["required"] = None
        out["required_label"] = "not required by the R-Codes if all deemed exempt provisions are met; scheme not checked"
        out["basis"] = row["note"] + " site.scheme_requires_da not supplied."
    else:
        out["required"] = False
        out["required_label"] = "not required if all deemed exempt provisions are met"
        out["basis"] = row["note"]
    return out


# --- consultation (Table 2.4) --------------------------------------------------------

def consultation(elements: list[str], chapter: str) -> list[dict[str, Any]]:
    t = _load("table-2.4.json")
    if chapter not in t["chapters"]:
        return []
    out = []
    for row in t["rows"]:
        el = row["elements"].get(chapter)
        if el and el in elements:
            out.append({"element": el, "element_title": row["element_title"], "parties": row["parties"],
                        "clauses": row.get("clauses"), "source": t["id"], "verify": row.get("verify", False)})
    return out


# --- permissions (Tables 2.5A, 2.5B, 3.5A; clause 2.5.2) ------------------------------

def permission(instrument_type: str, chapter: str, element: str, clause: str,
               direction: str | None, region: str | None) -> dict[str, Any]:
    """Best applicable permission row for a variation.

    Returns {"level": None} when the instrument type has no rights in this version.
    Otherwise the chosen row plus 'table'. When no row is applicable to the given
    direction/region, the best-ranked candidate is returned so the caller can say why.
    """
    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for table in _permission_tables():
        if instrument_type not in table["instruments"] or chapter not in table["chapters"]:
            continue
        rows = [r for r in table["rows"] if _row_matches(r, chapter, element)]
        specific = [r for r in rows if isinstance(r["clauses"], list) and clause in r["clauses"]]
        general = [r for r in rows if r["clauses"] == "all"]
        other = [r for r in rows if r["clauses"] == "other"]
        chosen = specific or general or other
        if not chosen:
            candidates.append((table, {"element": element, "clauses": "all", "permission": table["default"],
                                       "note": "table default (no row for this element)"}))
        for r in chosen:
            candidates.append((table, r))
    if not candidates:
        return {"level": None, "reason": f"{instrument_type} has no variation rights for {chapter} in this version"}

    def applicable(r: dict[str, Any]) -> bool:
        d = r.get("direction")
        if d and d != "any" and direction != d:
            return False
        if r["permission"] == "regional-lg" and region != "regional":
            return False
        return True

    ranked = sorted(candidates, key=lambda tr: PERMISSION_RANK[tr[1]["permission"]])
    ok = [tr for tr in ranked if applicable(tr[1])]
    table, row = (ok or ranked)[0]
    return {
        "level": row["permission"],
        "direction": row.get("direction"),
        "condition": row.get("condition"),
        "table": table["id"],
        "row": {"element": row.get("element"), "clauses": row.get("clauses")},
        "verify": bool(row.get("verify") or table.get("verify")),
        "note": row.get("note"),
    }


def _row_matches(row: dict[str, Any], chapter: str, element: str) -> bool:
    if row.get("chapters") and chapter not in row["chapters"]:
        return False
    return row["element"] in ("*", element)


def elements_with_rights(instrument_type: str, chapter: str) -> list[dict[str, Any]]:
    """For reports: every row that could apply to an instrument type and chapter."""
    out = []
    for table in _permission_tables():
        if instrument_type in table["instruments"] and chapter in table["chapters"]:
            out += [dict(r, table=table["id"]) for r in table["rows"] if _row_matches(r, chapter, r["element"])]
    return out
