"""Generate the recall layers of the published edition (spec section 5).

    python -m rcodes publish [--out edition]

Writes, under the output directory:

    README.md, CLAUDE.md, llms.txt      entry layer
    chapters/ch1/operation.md           Chapter 1 operation (Table 1.1, Figure 2.1, Table 2.4, clause 2.5.2)
    chapters/ch1/permissions.md         LPP/LDP permission levels per element (when too big for operation.md)
    chapters/<ch>/digest.md             one line per provision
    elements/<ch>/<element>.md          element packs
    indexes/                            facts-to-rules, elements-to-facts, rules.json, flagged.md
    definitions/                        Appendix A1, copied from Chapter 1 data
    records/<ch>/                       rule, fallback and table JSON, copied verbatim (ch1: operation data)

Everything is derived from the chapter packages; the output is deterministic (no dates,
sorted keys, LF line endings) so tests/test_edition.py can require the committed edition
to be byte-identical to a fresh run. Only the paths in MANAGED are owned by this
generator; other directories under the edition (graph/, schema/) are left alone.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import codings
from .ids import ClauseId
from .registry import PKG_ROOT, Registry
from .rules import ChapterPackage, Rule

REPO_ROOT = PKG_ROOT.parent.parent
VERSION = "draft-2026-10-24"
CHAPTERS = ["ch2", "ch3", "ch4p1", "ch4p2"]
CH1_DATA = PKG_ROOT / "chapters" / "ch1" / "data"

# Paths (relative to the edition root) this generator owns and rewrites.
MANAGED_DIRS = ["chapters", "elements", "indexes", "definitions", "records"]
MANAGED_FILES = ["README.md", "CLAUDE.md", "llms.txt"]

DIGEST_TARGET_TOKENS = (4000, 6000)
DIGEST_FAIL_TOKENS = 7000
PACK_TARGET_TOKENS = (1000, 5000)

KIND_ABBR = {"measurable": "m", "conditional": "c", "judgment": "j"}
FALLBACK_LABEL = {"M": "Merit assessment", "O": "Element objectives", "DG": "Design guidance"}

CH1_PERMISSION_FILES = ["table-2.5A.json", "table-2.5B.json", "table-3.5A.json"]
PERMISSION_LEVEL = {"without-wapc": "without WAPC approval", "regional-lg": "regional local governments only",
                    "wapc": "WAPC approval", "untabled": "untabled (clause 2.5.2)"}
CH1_OPERATION = "chapters/ch1/operation.md"
CH1_PERMISSIONS = "chapters/ch1/permissions.md"
CH1_OPERATION_TOKENS = 6000  # operation.md budget; above it the permission tables move to permissions.md

# Hand-written assessment skill at the edition root. Not generated and not managed (like graph/ and schema/);
# the entry files point to it.
SKILL = "SKILL.md"
# Hand-written governance notes (what governs, versions, verification, citation, corrections). Treated like SKILL.md.
GOVERNANCE = "GOVERNANCE.md"
# Hand-written worked example (edition/worked/). Not generated and not managed: publish never writes or deletes it.
WORKED = "worked/two-storey-r20-15x30.md"
TOPICS = "indexes/topics.md"

# Where local-variation questions go. README.md and CLAUDE.md both carry this sentence, so they cannot disagree.
LOCAL_VARIATION_POINTER = ("Local variation (what an LPP or LDP may vary, with or without WAPC approval, and under what "
                           "printed condition): the element pack's \"Local variation\" line, then `{perm}` for the "
                           "levels and row notes. When a development application is needed: `{op}` (Figure 2.1).")

# Rounding idioms in encoded formulas, explained in words beside them in the packs.
ROUNDING_WORDS = (("+ 0.001)", "nearest whole number, 0.5 rounds up"), ("+ 0.4999)", "rounded up"),
                  ("- 0.4999)", "rounded down"))

# Chapter 4 Part 2 element titles that name the same subject as a Chapter 2/3/4 Part 1 element (README element map).
ELEMENT_ALIASES = {"ch4p2": {"Side and rear setbacks": "Lot boundary setbacks", "Car and bicycle parking": "Parking",
                             "Tree canopy and deep soil areas": "Trees and landscaping", "Vehicle access": "Access",
                             "Private open space and balconies": "Private open space",
                             "Orientation": "Solar access for adjoining sites"}}

# indexes/topics.md: subject -> regular expression over rule titles (case-insensitive). A pattern starting
# "element:" matches element titles instead and lists every rule in the matching elements.
TOPIC_PATTERNS = [
    ("garage", r"\bgarage"),
    ("carport", r"\bcarport"),
    ("street setback", r"element:^street setbacks$"),
    ("side and rear setback", r"side setback|rear setback|lot boundary setback|setback from the boundary"),
    ("boundary wall", r"boundary wall"),
    ("site cover", r"site cover"),
    ("plot ratio", r"plot ratio"),
    ("height and storeys", r"building height|total building height|storeys|ridge height|wall height"),
    ("parking", r"parking|car spaces|\bbays?\b"),
    ("visitor parking", r"visitor"),
    ("bicycle", r"bicycle"),
    ("motorcycle and scooter", r"motorcycle|scooter"),
    ("tree", r"\btrees?\b"),
    ("deep soil", r"deep soil"),
    ("landscaping and planting", r"landscap|planting"),
    ("open space", r"open space|outdoor living|primary garden"),
    ("communal open space", r"communal open space"),
    ("privacy and overlooking", r"privacy|cone of vision|overlook|screen"),
    ("overshadowing", r"overshadow|shading|solar collector"),
    ("sunlight and daylight", r"\bsun|daylight|solar access|oriented north"),
    ("ventilation", r"ventilat"),
    ("fence", r"fenc"),
    ("driveway", r"driveway"),
    ("vehicle access", r"vehicle access|vehicle (opening|entr)|access point|battleaxe|sightline|forward gear"),
    ("pedestrian access", r"pedestrian"),
    ("storage", r"storage|\bstores\b"),
    ("waste and bins", r"waste|\bbins?\b"),
    ("utilities and services", r"utilit|services"),
    ("retaining walls and site works", r"retaining|site works|\bfill\b|excavation"),
    ("outbuilding", r"outbuilding"),
    ("ancillary dwelling", r"ancillary"),
    ("small dwelling", r"small dwelling"),
    ("dwelling size and rooms", r"floor area|bedroom|ceiling|living room|living space"),
    ("streetscape and facade", r"addresses the street|streetscape|fa\S{1,2}ade|outlook"),
    ("site area and frontage", r"site area|minimum frontage"),
    ("stormwater and water", r"stormwater|water"),
    ("universal design", r"universal|livable|silver level|gold-level"),
    ("building separation", r"separation"),
    ("noise", r"noise|acoustic"),
    ("energy", r"energy"),
]


def _ch1_table(t: dict[str, Any]) -> str:
    """'rcodes:.../ch1/T2.5A' -> 'Table 2.5A'."""
    tail = t["id"].rsplit("/", 1)[1]
    return "Table " + (tail[1:] if tail.startswith("T") else tail)


def lf(data: bytes) -> bytes:
    """Normalise line endings to LF, so sizes and output do not depend on the checkout."""
    return data.replace(b"\r\n", b"\n")


def tokens(text: str | bytes) -> int:
    """Token estimate used throughout the edition: UTF-8 bytes / 4, counted with LF line endings."""
    b = text.encode("utf-8") if isinstance(text, str) else text
    return len(lf(b)) // 4


# --- small text helpers ------------------------------------------------------------

def _ws(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _short(text: str, n: int) -> str:
    text = _ws(text)
    return text if len(text) <= n else text[: n - 1].rstrip(" ,;:(") + "…"


def short_id(rule_id: str) -> str:
    cid = ClauseId.parse(rule_id)
    return cid.clause + (f"#{cid.fragment}" if cid.fragment else "")


def ref_id(rule_id: str | None, chapter: str) -> str:
    """Short form of a cross-reference; chapter-qualified when it leaves the chapter."""
    if not rule_id:
        return ""
    cid = ClauseId.parse(rule_id)
    s = short_id(rule_id)
    return s if cid.chapter == chapter else f"{cid.chapter}/{s}"


_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50}


def _roman(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s):
        v = _ROMAN.get(ch, 0)
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def _natural(s: str) -> tuple:
    s = re.sub(r"\(([ivxl]+)\)", lambda m: "(%03d)" % _roman(m.group(1)), s)
    return tuple(int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s) if t != "")


_CLAUSE = re.compile(r"^(?P<col>[A-Z]+)?(?P<nums>\d+(?:\.\d+)*)(?P<rest>.*)$")


def clause_key(rule_id: str) -> tuple:
    cid = ClauseId.parse(rule_id)
    m = _CLAUSE.match(cid.clause)
    if not m:
        return ((9999,), _natural(cid.clause), _natural(cid.fragment or ""))
    nums = tuple(int(x) for x in m["nums"].split("."))
    col_rank = {"T": 0}.get(m["col"] or "", 1)
    return (nums, col_rank, _natural(m["rest"]), _natural(cid.fragment or ""))


def element_key(element: str) -> tuple:
    return tuple(int(x) if x.isdigit() else x for x in element.split("."))


def page_of(doc: dict[str, Any]) -> str:
    src = doc.get("source") or {}
    p = src.get("page")
    return "" if p is None else str(p)


def coding_text(coding: list[str] | None, chapter_coding: list[str]) -> str:
    if not coding or coding == ["all"] or list(coding) == list(chapter_coding):
        return "all"
    return ",".join(coding)


# --- fact vocabulary -----------------------------------------------------------------

@dataclass
class Fact:
    name: str
    type: str
    meaning: str
    chapter: str


def parse_facts(path: Path, chapter: str) -> dict[str, Fact]:
    out: dict[str, Fact] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "Fact":
            continue
        names, typ, meaning = cells[0], cells[1], " | ".join(cells[2:]).strip()
        for n in names.split(","):
            n = n.strip().strip("`").strip()
            if n and n not in out:
                out[n] = Fact(n, typ, meaning, chapter)
    return out


class Vocabulary:
    def __init__(self, by_chapter: dict[str, dict[str, Fact]]):
        self.by_chapter = by_chapter
        self.unknown: set[str] = set()

    def get(self, name: str, chapter: str) -> Fact | None:
        f = self.by_chapter.get(chapter, {}).get(name)
        if f:
            return f
        for ch in CHAPTERS:
            f = self.by_chapter.get(ch, {}).get(name)
            if f:
                return f
        for ch in [chapter] + CHAPTERS:  # placeholder entries such as landscape.on_structure.<type>.provided
            for key, f in self.by_chapter.get(ch, {}).items():
                if "<" in key and re.fullmatch(re.sub(r"<[^>]+>", "[A-Za-z0-9_]+", re.escape(key)), name):
                    return f
        self.unknown.add(name)
        return None


def _humanise(name: str) -> str:
    leaf = re.sub(r"_(m|m2|mm|pct|deg|count)$", "", name)
    return leaf.replace(".", " ").replace("_", " ")


def _unit_of(name: str) -> str:
    for suf, unit in (("_m2", "m²"), ("_mm", "mm"), ("_m", "m"), ("_pct", "%"), ("_deg", "°"), ("_l", "L"),
                      ("_kl", "kL"), ("_m3", "m³")):
        if name.endswith(suf):
            return unit
    return ""


def question(f: Fact | None, name: str) -> str:
    """A question for the applicant: the fact's short name, unit and FACTS.md meaning."""
    human = _humanise(name.split(".", 1)[1] if "." in name else name)
    meaning = _ws(f.meaning) if f and f.meaning else ""
    typ = (f.type if f else "").strip()
    unit = _unit_of(name)
    if typ == "bool":
        if meaning:
            return f"{meaning[0].upper() + meaning[1:]}? (yes/no)"
        return f"{human[0].upper() + human[1:]}? (yes/no)"
    hint = "; ".join(x for x in (unit or (typ if typ not in ("number", "int", "count") else ""), meaning) if x)
    return f"What is the {human}?" + (f" ({hint})" if hint else "")


# --- definitions ------------------------------------------------------------------

class Definitions:
    def __init__(self, doc: dict[str, Any]):
        self.terms: dict[str, dict[str, Any]] = {}
        for t in doc["terms"]:
            for key in [t["term"], *(t.get("aliases") or [])]:
                self.terms.setdefault(key.lower().strip(), t)
        self.missing: set[str] = set()

    def get(self, term: str) -> dict[str, Any] | None:
        k = term.lower().strip()
        t = self.terms.get(k)
        if t is None and k.endswith("s"):
            t = self.terms.get(k[:-1])
        if t is None:
            self.missing.add(term)
        return t


# --- evaluator phrases -------------------------------------------------------------

def _num(v: Any) -> str:
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float) and v.is_integer():
        return f"{v:.1f}"
    return str(v)


def table_name(ref: str, short: bool = False) -> str:
    return "Table " + (ref[6:] if ref.startswith("table-") else ref)


def _keys_phrase(table: dict[str, Any] | None, short: bool = False) -> str:
    if not table:
        return ""
    if short and [k for k in table.get("keys", [])] == ["site.r_code"]:
        return ""
    ks = ["coding" if k.endswith("r_code") else k.rsplit(".", 1)[-1] for k in table.get("keys", [])]
    return " by " + ",".join(ks) if ks else ""


def value_phrase(v: Any, fact: str | None, tables, short: bool = False) -> str:
    if isinstance(v, dict) and "fact" in v:
        return v["fact"]
    if isinstance(v, dict) and "table" in v:
        return table_name(v["table"]) + _keys_phrase(tables(v["table"]), short)
    if v is None:
        return "(no value)"
    unit = _unit_of(fact or "")
    s = _num(v)
    return f"{s} {unit}".strip() if unit and unit != "%" else (s + unit if unit else s)


def phrase(spec: dict[str, Any] | None, tables, depth: int = 0, short: bool = False) -> str:
    """The test in a few words: '>= 5.0 m', '<= Table 3.1a by coding', 'yes', 'judgment'."""
    if not spec:
        return "judgment"
    t = spec.get("type")
    op = spec.get("op", ">=" if t in ("threshold", "count") else "<=")
    if t in ("threshold", "count"):
        p = f"{op} {value_phrase(spec.get('value'), spec.get('fact'), tables, short)}"
        return p if short else f"{spec['fact']} {p}"
    if t == "boolean":
        p = "yes" if spec.get("expected", True) else "no"
        return p if short else f"{spec['fact']} = {p}"
    if t == "percentage-of":
        v = spec.get("value")
        vp = value_phrase(v, None, tables) + ("%" if not isinstance(v, dict) else "")
        p = f"{op} {vp} of {spec['of']}"
        return p if short else f"{spec['fact']} as % of {spec['of']} {op} {vp}"
    if t == "table-lookup":
        table = tables(spec["table"])
        tp = table_name(spec["table"], short) + _keys_phrase(table, short)
        if "fact" not in spec:
            return f"{tp} gives yes"
        return f"{op} {tp}" if short else f"{spec['fact']} {op} {tp}"
    if t == "formula":
        expr = spec["expr"]
        if "value" not in spec and "op" not in spec:
            return expr
        v = spec.get("value")
        vp = v if isinstance(v, str) else value_phrase(v, None, tables)
        return f"{expr} {spec.get('op', '>=')} {vp}"
    if t == "composite":
        mode = spec.get("mode", "all")
        parts = [phrase(p, tables, depth + 1, short=False) for p in spec["parts"]]
        if short:
            inner = "; ".join(phrase(p, tables, depth + 1, short=True) for p in spec["parts"])
            return f"{mode}({inner})" if len(inner) <= 48 else f"{mode} of {len(parts)} tests"
        joiner = " AND " if mode == "all" else " OR "
        return "(" + joiner.join(parts) + ")"
    if t == "geometry":
        return f"{spec.get('measure')} of {spec.get('geometry')} {op} {value_phrase(spec.get('value'), None, tables)}"
    return str(t)


def effect_phrase(effect: dict[str, Any], tables) -> str:
    if not effect:
        return "no effect stated"
    if effect.get("not_applicable"):
        return "the provision does not apply"
    if "replace_evaluator" in effect:
        return "test becomes: " + phrase(effect["replace_evaluator"], tables)
    if "set" in effect:
        bits = []
        for k, v in effect["set"].items():
            bits.append(f"{k} = {value_phrase(v, None, tables) if not isinstance(v, (str, list)) else v}")
        return "sets " + ", ".join(bits)
    return json.dumps(effect, ensure_ascii=False, sort_keys=True)


# --- table inlining ----------------------------------------------------------------

_ALL_CODES = codings.NUMERIC + codings.NAMED


def _band_codes(band: Any) -> set[str]:
    bands = band if isinstance(band, list) else [band]
    return {c for c in _ALL_CODES if any(isinstance(b, str) and codings.in_band(c, b) for b in bands)}


def _match_text(k: str, want: Any) -> str:
    if isinstance(want, list):
        return "/".join(_match_text(k, w) for w in want)
    if isinstance(want, dict) and ("min" in want or "max" in want):
        lo, hi = want.get("min"), want.get("max")
        if lo is not None and hi is not None:
            return f"{_num(lo)}-{_num(hi)}"
        return f">= {_num(lo)}" if lo is not None else f"<= {_num(hi)}"
    return _num(want)


def table_rows_text(table: dict[str, Any], rule_coding: list[str] | None) -> list[str]:
    keys = table.get("keys", [])
    unit = table.get("unit") or ""
    rule_codes = _band_codes(rule_coding or ["all"])
    out = []
    for row in table.get("rows", []):
        match = row.get("match", {})
        rc = next((match[k] for k in match if k.endswith("r_code")), None)
        if rc is not None and not (_band_codes(rc) & rule_codes):
            continue
        cond = ", ".join(
            (_match_text(k, match[k]) if k.endswith("r_code") else f"{k.rsplit('.', 1)[-1]} {_match_text(k, match[k])}")
            for k in keys if k in match)
        v = row.get("value")
        val = "no provision" if v is None else (f"{_num(v)} {unit}".strip() if not isinstance(v, (dict, list)) else
                                                json.dumps(v, ensure_ascii=False, sort_keys=True))
        note = f" ({_ws(row['note'])})" if row.get("note") else ""
        out.append(f"{cond or 'any'}: {val}{note}")
    if "default" in table:
        out.append(f"otherwise: {_num(table['default'])} {unit}".strip())
    return out


def tables_in(spec: Any) -> list[str]:
    found: list[str] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            if x.get("type") == "table-lookup" and "table" in x:
                found.append(x["table"])
            elif "table" in x and isinstance(x["table"], str) and set(x) <= {"table"}:
                found.append(x["table"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(spec)
    seen: list[str] = []
    for t in found:
        if t not in seen:
            seen.append(t)
    return seen


# --- the edition -------------------------------------------------------------------

@dataclass
class Edition:
    reg: Registry
    out: Path
    files: dict[str, bytes] = field(default_factory=dict)
    unplaced: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.pkgs: dict[str, ChapterPackage] = {}
        for ch in CHAPTERS:
            pkg = self.reg.package(VERSION, ch)
            if pkg is None:
                raise KeyError(f"chapter package {ch} not loaded")
            self.pkgs[ch] = pkg
        self.vocab = Vocabulary({ch: parse_facts(p.root / "FACTS.md", ch) for ch, p in self.pkgs.items()
                                 if (p.root / "FACTS.md").exists()})
        self.a1_doc = json.loads((CH1_DATA / "definitions-A1.json").read_text(encoding="utf-8"))
        self.defs = Definitions(self.a1_doc)
        self.t11 = json.loads((CH1_DATA / "table-1.1.json").read_text(encoding="utf-8"))

    # helpers
    def tables(self, ch: str):
        return self.reg.table_resolver(VERSION, ch)

    def put(self, rel: str, text: str) -> None:
        self.files[rel] = lf(text.encode("utf-8"))

    def rules_by_element(self, ch: str) -> dict[str, list[Rule]]:
        pkg = self.pkgs[ch]
        out: dict[str, list[Rule]] = {}
        for r in pkg.rules.values():
            out.setdefault(r.element, []).append(r)
        for v in out.values():
            v.sort(key=lambda r: clause_key(r.id))
        return out

    def fallbacks_by_element(self, ch: str) -> dict[str, list[Rule]]:
        out: dict[str, list[Rule]] = {}
        for r in self.pkgs[ch].fallbacks.values():
            out.setdefault(r.element, []).append(r)
        order = {"M": 0, "O": 0, "DG": 2}
        for v in out.values():
            v.sort(key=lambda r: (order.get(r.column, 1), clause_key(r.id)))
        return out

    def elements(self, ch: str) -> list[str]:
        pkg = self.pkgs[ch]
        els = set(pkg.meta.get("elements", {})) | {r.element for r in pkg.rules.values()} | \
            {r.element for r in pkg.fallbacks.values()}
        return sorted(els, key=element_key)

    def element_title(self, ch: str, el: str) -> str:
        t = self.pkgs[ch].meta.get("elements", {}).get(el)
        if t:
            return t
        for r in list(self.pkgs[ch].rules.values()) + list(self.pkgs[ch].fallbacks.values()):
            if r.element == el:
                return r.data.get("element_title", "")
        return ""

    def record_path(self, r: Rule, ch: str) -> str:
        rel = r.path.relative_to(self.pkgs[ch].root).as_posix() if r.path else ""
        return f"records/{ch}/{rel}"

    def flag_note(self, d: dict[str, Any]) -> str:
        return _ws((d.get("verified") or {}).get("note") or d.get("notes") or "")

    # -- layers --------------------------------------------------------------------
    def build(self) -> None:
        self.build_ch1()
        for ch in CHAPTERS:
            self.build_digest(ch)
            self.build_packs(ch)
            self.copy_records(ch)
        self.build_indexes()
        self.copy_definitions()
        self.build_entry()

    def copy_records(self, ch: str) -> None:
        root = self.pkgs[ch].root
        for sub in ("rules", "fallbacks", "tables"):
            d = root / sub
            if not d.exists():
                continue
            for p in sorted(d.rglob("*.json")):
                self.files[f"records/{ch}/{p.relative_to(root).as_posix()}"] = lf(p.read_bytes())

    def copy_definitions(self) -> None:
        self.files["definitions/A1.json"] = lf((CH1_DATA / "definitions-A1.json").read_bytes())
        self.files["definitions/A1.md"] = lf((CH1_DATA / "definitions-A1.md").read_bytes())

    # digest ------------------------------------------------------------------------
    def coding_domain(self, ch: str) -> set[str]:
        if not hasattr(self, "_domains"):
            self._domains: dict[str, set[str]] = {}
        if ch not in self._domains:
            dom: set[str] = set()
            generic = {"all", "numeric", "named"}
            for r in self.pkgs[ch].rules.values():
                bands = r.data.get("coding") or ["all"]
                dom |= _band_codes([b for b in bands if b.lower() not in generic])
                if any(b.lower() in ("all", "numeric") for b in bands):
                    dom |= set(codings.NUMERIC)
            self._domains[ch] = dom
        return self._domains[ch]

    def coding_compact(self, ch: str, coding: list[str] | None) -> str:
        """Shortest of: 'all', 'all but X', a collapsed band list, the record's own list."""
        dom = self.coding_domain(ch)
        codes = _band_codes(coding or ["all"]) & dom
        if codes == dom:
            return "all"
        cands = [",".join(coding or ["all"]), _collapse(codes)]
        rest = dom - codes
        if len(rest) <= 3:
            cands.append("all but " + _collapse(rest))
        return min(cands, key=len)

    def digest_line(self, r: Rule, ch: str, el_fallback: str | None, el_coding: str | None = None,
                    title: str | None = None) -> str:
        d = r.data
        pkg = self.pkgs[ch]
        tables = self.tables(ch)
        facts = [n for n in r.inputs if n != "site.r_code"]
        bits = [f"- `{short_id(r.id)}` {title or _digest_title(d['title'], d.get('region'))}",
                KIND_ABBR.get(r.kind, r.kind) + ("" if r.column in ("C", "A") else f"/{r.column}"),
                "=" if self.coding_compact(ch, d.get("coding")) == el_coding else self.coding_compact(ch, d.get("coding")),
                _facts_count(facts),
                _short_words(phrase(r.evaluator, tables, short=True), 36)]
        exc = r.exceptions
        if exc:
            tags: list[str] = []
            for e in exc:
                if _exc_tag(e) not in tags:
                    tags.append(_exc_tag(e))
            bits.append(f"exc {len(exc)}: " + ",".join(tags))
        fb = ref_id(r.fallback, ch)
        if fb and fb != el_fallback:
            bits.append(f"fb {fb}")
        line = ";".join(bits)
        if d.get("verify"):
            line += " ⚑"
        return line

    def build_digest(self, ch: str) -> None:
        pkg = self.pkgs[ch]
        meta = pkg.meta
        by_el = self.rules_by_element(ch)
        fb_el = self.fallbacks_by_element(ch)
        n_rules = len(pkg.rules)
        n_flag = sum(1 for r in pkg.rules.values() if r.data.get("verify"))
        test_col = meta.get("columns", {}).get("testable", "C")
        fb_col = meta.get("columns", {}).get("fallback", "M")
        pathway = meta.get("pathway", "")
        lines = [
            f"# {meta['title']}: digest",
            "",
            f"Version {VERSION}. Applies to {', '.join(meta.get('dwelling_types', []))}; coding "
            f"{coding_text(meta.get('coding'), [])}; pathway {pathway}. {n_rules} provisions, {n_flag} flagged ⚑.",
            f"Testable column {test_col}; a provision not met falls back to the element's {fb_col} record"
            + (" (DG informs it)" if ch == "ch4p2" else "") + f". Full text: `elements/{ch}/<element>.md`.",
            "",
            "Line, fields split by `;`: `ID` title; kind (m measurable, c conditional, j judgment; /col if not "
            f"{test_col}); coding (= as heading); facts (count and the first two; the full list is under the "
            "provision's heading in the pack); test (a table is looked up by coding unless `by` says otherwise); exc n: "
            "labels; fb (fallback) if not the element's; ⚑ verify. `site.r_code` is implied by every coding and "
            "is not counted.",
            "Find a provision in its pack by grepping for its heading, e.g. ``^### `C3.3.1` ``, and read that section only.",
        ]
        if meta.get("notes"):
            lines += ["", "Note: " + _short_words(meta["notes"], 200)]
        for el in self.elements(ch):
            rules = by_el.get(el, [])
            fbs = [f for f in fb_el.get(el, []) if f.column in ("M", "O")]
            el_fb = short_id(fbs[0].id) if fbs else None
            if not rules:
                if el_fb or fb_el.get(el):
                    lines += ["", f"## {el} {self.element_title(ch, el)} (no {test_col} provisions; "
                              f"{', '.join(short_id(f.id) for f in fb_el.get(el, []))})"]
                continue
            cods = [self.coding_compact(ch, r.data.get("coding")) for r in rules]
            el_cod = max(sorted(set(cods)), key=lambda c: (cods.count(c), -len(c)))
            lines += ["", f"## {el} {self.element_title(ch, el)} (coding {el_cod}" + (f"; fb {el_fb})" if el_fb else ")")]
            titles = _distinct_titles(rules, lambda r: self.coding_compact(ch, r.data.get("coding")))
            lines += [self.digest_line(r, ch, el_fb, el_cod, titles[r.id]) for r in rules]
        self.put(f"chapters/{ch}/digest.md", "\n".join(lines) + "\n")

    # element packs -----------------------------------------------------------------
    def build_packs(self, ch: str) -> None:
        pkg = self.pkgs[ch]
        by_el = self.rules_by_element(ch)
        fb_el = self.fallbacks_by_element(ch)
        tables = self.tables(ch)
        for el in self.elements(ch):
            rules = by_el.get(el, [])
            fbs = fb_el.get(el, [])
            if not rules and not fbs:
                continue
            seen: dict[str, str] = {}
            title = self.element_title(ch, el)
            L = [f"# {pkg.meta['title']}: element {el} {title}", "",
                 f"Version {VERSION}. {len(rules)} provisions. Digest: `chapters/{ch}/digest.md`. "
                 f"Records: `records/{ch}/`. ⚑ = still flagged verify. Each provision is headed "
                 "``### `ID` title`` with its facts on the next line; grep the ID and stop there if that is enough.", ""]
            lv = self.local_variation_line(ch, el)
            if lv:
                L += [lv, ""]
            head = [f for f in fbs if f.column != "DG"]
            tail = [f for f in fbs if f.column == "DG"]
            for f in head:
                L += self.fallback_block(f, ch)
            # questions
            facts: list[str] = []
            for r in rules:
                for n in r.inputs:
                    if n not in facts:
                        facts.append(n)
            if facts:
                L += ["## Questions to ask the applicant", ""]
                for n in facts:
                    L.append(f"- `{n}`: {question(self.vocab.get(n, ch), n)}")
                L.append("")
            L += ["## Provisions", ""]
            for r in rules:
                L += self.provision_block(r, ch, tables, seen)
            for f in tail:
                L += self.fallback_block(f, ch)
            self.put(f"elements/{ch}/{el}.md", _rounding_words("\n".join(L).rstrip("\n") + "\n"))

    def fallback_block(self, f: Rule, ch: str) -> list[str]:
        d = f.data
        label = FALLBACK_LABEL.get(f.column, f.column)
        L = [f"## {label} `{short_id(f.id)}`: {_ws(d['title'])}", "",
             _ws(d.get("text")) or "(no text captured)", "",
             f"Source p{page_of(d)}." + (f" ⚑ {self.flag_note(d)}" if d.get("verify") else ""), ""]
        return L

    def provision_block(self, r: Rule, ch: str, tables, seen: dict[str, str]) -> list[str]:
        d = r.data
        pkg = self.pkgs[ch]
        L = [f"### `{short_id(r.id)}` {_ws(d['title'])}" + (" ⚑" if d.get("verify") else ""), "",
             "Facts: " + (", ".join(f"`{n}`" for n in r.inputs) if r.inputs else "none (judgment against the text)")
             + ".", ""]
        L.append(f"Kind {r.kind}; column {r.column}; coding {coding_text(d.get('coding'), pkg.meta.get('coding', []))}; "
                 f"applies to {', '.join(d.get('applies_to') or ['any'])}"
                 + (f"; region {d['region']}" if d.get("region", "all") != "all" else "")
                 + f"; source p{page_of(d)}" + (f" {d['source']['table']}" if (d.get("source") or {}).get("table") else "")
                 + ".")
        text = _ws(d.get("text")) or "(no text captured)"
        first = seen.setdefault("text:" + text, short_id(r.id))
        if first != short_id(r.id):
            L += ["", f"> (printed text as for `{first}` above)", ""]
        else:
            L += ["", "> " + text, ""]
        test = phrase(r.evaluator, tables) if r.evaluator else "judgment: no encoded test; assess against the text"
        L.append(f"Test: {test}.")
        for t in tables_in(r.evaluator):
            table = tables(t)
            if not table:
                L.append(f"- {table_name(t)}: not found")
                continue
            rows = table_rows_text(table, d.get("coding"))
            tkey = f"table:{t}:" + "; ".join(rows)
            if tkey in seen:
                L.append(f"- {table_name(t)}: rows as under `{seen[tkey]}` above.")
                continue
            seen[tkey] = short_id(r.id)
            L.append(f"- {table_name(t)} ({_ws(table.get('title', ''))}): " + "; ".join(rows) + "."
                     + (" ⚑ table flagged" if table.get("verify") else ""))
        if r.conditions:
            L.append("Applies only when: " + "; ".join(phrase(c, tables) for c in r.conditions) + ".")
        for i, e in enumerate(r.exceptions, 1):
            L.append(f"Exception {i}: {_ws(e.get('label'))}. When {phrase(e.get('condition'), tables)}: "
                     f"{effect_phrase(e.get('effect') or {}, tables)}."
                     + (f" ({_ws(e['source'])})" if e.get("source") else "") + (" ⚑" if e.get("verify") else ""))
        if r.fallback:
            L.append(f"Not met: assess against `{ref_id(r.fallback, ch)}`.")
        terms = []
        for term in d.get("defined_terms") or []:
            key = "term:" + term.lower().strip()
            if key in seen:
                continue
            seen[key] = short_id(r.id)
            t = self.defs.get(term)
            if t:
                terms.append(f"- *{t['term']}* (A1 p{t.get('page', '')}): {_ws(t['definition'])}")
        if terms:
            L.append("Defined terms:")
            L += terms
        if d.get("verify"):
            L.append(f"⚑ Verification note: {self.flag_note(d) or 'flagged; no note'}")
        L.append("")
        return L

    # chapter 1 operation layer -------------------------------------------------------
    def ch1(self, name: str) -> dict[str, Any]:
        return json.loads((CH1_DATA / name).read_text(encoding="utf-8"))

    def perm_tables(self, ch: str) -> list[tuple[str, dict[str, Any]]]:
        """(label, table) for the LPP/LDP permission tables that cover a chapter."""
        out = []
        for name in CH1_PERMISSION_FILES:
            t = self.ch1(name)
            if ch not in t["chapters"]:
                continue
            ins = t["instruments"]
            label = "LPP and LDP" if set(ins) == {"lpp", "ldp"} else ("LPP" if ins == ["lpp"] else "LDP")
            out.append((label, t))
        return out

    def perm_cell(self, table: dict[str, Any], ch: str, el: str) -> str:
        """What a table lets the instrument do with one element: each row as 'clauses: level (condition)'.
        Rows are those rcodes.chapters.ch1.operation.elements_with_rights would return for the element."""
        rows = [r for r in table["rows"] if r["element"] == el and (not r.get("chapters") or ch in r["chapters"])]
        if not rows:
            return f"not listed: {PERMISSION_LEVEL[table['default']]} (table default)"
        parts = []
        sole = all(isinstance(r["clauses"], str) for r in rows)  # 'other' with no clause rows for this chapter
        listed = [", ".join(r["clauses"]) for r in rows if isinstance(r["clauses"], list)]
        nth: dict[str, int] = {}
        for r in rows:
            cl = r["clauses"]
            ctext = ({"all": "all clauses", "other": "all clauses" if sole else "other clauses"}.get(cl)
                     if isinstance(cl, str) else ", ".join(cl))
            if isinstance(cl, list) and listed.count(ctext) > 1:
                nth[ctext] = nth.get(ctext, 0) + 1
                ctext = f"{ctext} (row {nth[ctext]} of {listed.count(ctext)})"
            bit = f"{ctext or cl}: {PERMISSION_LEVEL[r['permission']]}"
            if r.get("condition"):
                bit += f" ({_ws(r['condition']).rstrip('.')})"
            elif r.get("direction") in ("increase", "decrease"):
                bit += f" ({r['direction']} only)"
            elif isinstance(cl, list):
                bit += " (no printed condition)"
            parts.append(bit + (" ⚑" if r.get("verify") else ""))
        if all(isinstance(r["clauses"], list) for r in rows):
            parts.append(f"other clauses: {PERMISSION_LEVEL[table['default']]} (table default)")
        return "; ".join(parts)

    def local_variation_line(self, ch: str, el: str) -> str:
        bits = [f"{label} ({_ch1_table(t)}): {self.perm_cell(t, ch, el)}" for label, t in self.perm_tables(ch)]
        if not bits:
            return ""
        tail = (" Schemes and precinct structure plans: clause 2.5.2."
                if ch in self.ch1("clause-2.5.2.json")["chapters"] else "")
        return "Local variation (Chapter 1): " + ". ".join(bits) + "." + tail + f" Levels and notes: `{self.ch1_perm_path}`."

    def build_ch1(self) -> None:
        for p in sorted(CH1_DATA.glob("*.json")):
            if not p.name.startswith("definitions"):
                self.files[f"records/ch1/{p.name}"] = lf(p.read_bytes())
        perm = self.ch1_permissions()
        op = self.ch1_operation(split=False, perm=perm)
        self.ch1_perm_path = CH1_OPERATION
        if tokens(op) > CH1_OPERATION_TOKENS:
            op = self.ch1_operation(split=True, perm=perm)
            self.put(CH1_PERMISSIONS, perm)
            self.ch1_perm_path = CH1_PERMISSIONS
        self.put(CH1_OPERATION, op)

    def ch1_permissions(self) -> str:
        L = ["# Chapter 1: local variation of Chapters 2, 3 and 4 by LPP and LDP", "",
             f"Version {VERSION}. Generated from the Chapter 1 permission tables as encoded "
             "(`records/ch1/table-2.5A.json`, `table-2.5B.json`, `table-3.5A.json`). For each element: what a local "
             "planning policy (LPP) and a local development plan (LDP) may vary, and at what level. Schemes and "
             f"precinct structure plans: clause 2.5.2 in `{CH1_OPERATION}`.", "",
             "Levels: **without WAPC approval**; **regional local governments only** (without WAPC approval, but only "
             "by local governments outside the Perth and Peel regions; in Perth and Peel it needs WAPC approval); "
             "**WAPC approval** (prior approval of the WAPC required). The printed condition follows in brackets. "
             "\"Unless otherwise specified, any modification that does not satisfy the applicable conditions "
             "identified in Table 2.5A and 2.5B requires the prior approval of the WAPC\" (p11). Table 2.5B has no "
             "conditions column, so a permitted LDP variation runs in either direction. ⚑ = row flagged verify (a "
             "merged, blank, uncoloured or misnumbered cell on the page); see the notes at the end.", ""]
        notes: dict[tuple[str, str], list[str]] = {}
        for ch in CHAPTERS:
            tabs = self.perm_tables(ch)
            if not tabs:
                continue
            labels = [f"{lab} ({_ch1_table(t)}, p{page_of(t)})" for lab, t in tabs]
            L += [f"## {self.pkgs[ch].meta['title']} ({ch})", "",
                  "| Element | " + " | ".join(labels) + " |", "|---|" + "---|" * len(tabs)]
            for el in self.elements(ch):
                L.append(f"| {el} {self.element_title(ch, el)} | "
                         + " | ".join(self.perm_cell(t, ch, el) for _, t in tabs) + " |")
                for _, t in tabs:
                    for r in t["rows"]:
                        if r["element"] == el and r.get("note") and (not r.get("chapters") or ch in r["chapters"]):
                            head = (f"{_ch1_table(t)} {r['element']} {r.get('element_title', '')}"
                                    + (f" ({r['register_ref']})" if r.get("register_ref") else ""))
                            chs = notes.setdefault((head, _ws(r["note"])), [])
                            if ch not in chs:
                                chs.append(ch)
            L.append("")
            if ch == "ch4p2":
                L += ["Chapter 1B 3.5.2: LPPs and LDPs may amend or replace Acceptable Outcomes in accordance with the "
                      "table where warranted by specific need, consistent with the Element Objectives, and able to be "
                      "implemented and audited. Elements 2.2 to 2.7 share one printed cell, \"All of Section 2 key "
                      "development parameters (height, plot ratio, setbacks)\". Chapter 1B gives schemes and precinct "
                      "structure plans no right equivalent to clause 2.5.2.", ""]
        L += ["## Notes on rows", ""]
        for (head, note), chs in notes.items():
            L.append(f"- {head} [{', '.join(chs)}]: {note}")
        return "\n".join(L).rstrip("\n") + "\n"

    def ch1_operation(self, split: bool, perm: str) -> str:
        t11, f21, t24, c252 = (self.ch1(n) for n in ("table-1.1.json", "figure-2.1.json", "table-2.4.json",
                                                      "clause-2.5.2.json"))
        L = ["# Chapter 1 Operation of the Code: operation layer", "",
             f"Version {VERSION}. Generated from the Chapter 1 data files (copied verbatim to `records/ch1/`), "
             f"source *{t11['source']['file']}*; page numbers are printed pages. Contents: Table 1.1 (which "
             "chapter applies), Figure 2.1 (when a development application is required), Table 2.4 (consultation), "
             "local variation by LPP and LDP (Tables 2.5A, 2.5B, 3.5A), clause 2.5.2 (schemes and precinct structure "
             "plans). Definitions: `definitions/A1.md`. ⚑ = flagged verify.", ""]
        L += [f"## {t11['title']}", "", f"`{t11['id']}`, clause {t11['source']['clause']}, p{page_of(t11)}.", "",
              "| Dwelling type | Coding | Chapter | Pathway |", "|---|---|---|---|"]
        for r in t11["rows"]:
            L.append(f"| {r['dwelling_type'].replace('_', ' ')} | {', '.join(r['coding'])} | "
                     f"{r.get('chapter') or 'none (not provided for)'} | {r.get('pathway') or '-'} |")
        L += ["", "Printed text:", ""]
        for r in t11["rows"]:
            L.append(f"- {r['dwelling_type'].replace('_', ' ')}, {', '.join(r['coding'])}: \"{_ws(r['text'])}\""
                     + (f" Note: {_ws(r['note'])}" if r.get("note") else ""))
        L += ["", f"Footnote: \"{_ws(t11['footnote_text'])}\" Chapter 1A operates Chapters 2, 3 and 4 Part 1; "
              "Chapter 1B operates Chapter 4 Part 2.", ""]
        L += [f"## {f21['title']}", "", f"`{f21['id']}`, clause {f21['source']['clause']}, p{page_of(f21)}. "
              "When a development application (DA) is required.", "",
              "| Dwelling type | DA required when all deemed exempt provisions are met |", "|---|---|"]
        for r in f21["rows"]:
            L.append(f"| {r['dwelling_type'].replace('_', ' ')} | "
                     f"{'yes' if r['required'] else 'no, unless the scheme requires one'} |")
        L += [""] + [f"- {r['dwelling_type'].replace('_', ' ')}: \"{_ws(r['text'])}\" {_ws(r['note'])}" for r in f21["rows"]]
        L += [f"- Merit: \"{_ws(f21['merit_text'])}\"", f"- Basis: {_ws(f21['basis'])}", ""]
        chs = t24["chapters"]
        L += [f"## {t24['title']}", "", f"`{t24['id']}`, clause {t24['source']['clause']}, p{page_of(t24)}. "
              f"{_ws(t24['notes'])}", "",
              "| Element | " + " | ".join(chs) + " | Clauses | Consult |", "|---|" + "---|" * len(chs) + "---|---|"]
        for r in t24["rows"]:
            L.append(f"| {r['element_title']} | " + " | ".join(r["elements"].get(c, "-") for c in chs)
                     + f" | {', '.join(r.get('clauses') or ['all'])} | {r['parties']}"
                     + (" ⚑" if r.get("verify") else "") + " |")
        noted = [r for r in t24["rows"] if r.get("note")]
        if noted:
            L += [""] + [f"- {r['element_title']}{' ⚑' if r.get('verify') else ''}: {_ws(r['note'])}" for r in noted]
        L.append("")
        L += ["## Local variation by LPP and LDP (Tables 2.5A, 2.5B, 3.5A)", ""]
        for n in CH1_PERMISSION_FILES:
            t = self.ch1(n)
            L.append(f"- `{t['id']}` {t['title']}: {', '.join(t['instruments']).upper()}; chapters "
                     f"{', '.join(t['chapters'])}; clause {t['source']['clause']}, p{page_of(t)}; not listed: "
                     f"{PERMISSION_LEVEL[t['default']]}.")
        L.append("")
        if split:
            L += ["Per chapter and element, what an LPP and an LDP may vary and at what level (without WAPC approval, "
                  "regional local governments only, WAPC approval), with the printed condition and flagged rows: "
                  f"`{CH1_PERMISSIONS}`. Each element pack repeats its element's line under the title "
                  "(\"Local variation\").", ""]
        else:
            body = perm.split("\n", 2)[2]
            L += [re.sub(r"^## ", "### ", body, flags=re.M), ""]
        row = c252["rows"][0]
        L += [f"## {c252['title']}", "", f"`{c252['id']}`, p{page_of(c252)}. Instruments: local planning scheme, "
              f"precinct structure plan. Chapters: {', '.join(c252['chapters'])} (Chapter 1A; Chapter 1B 3.5 gives "
              "no equivalent for ch4p2). Not subject to Tables 2.5A or 2.5B; the engine reports such a variation as "
              f"untabled. ⚑ {_ws(row['note'])}", ""]
        return "\n".join(L).rstrip("\n") + "\n"

    # indexes -----------------------------------------------------------------------
    def build_indexes(self) -> None:
        f2r: dict[str, dict[str, Any]] = {}
        e2f: dict[str, dict[str, Any]] = {}
        rules_idx: list[dict[str, Any]] = []
        for ch in CHAPTERS:
            pkg = self.pkgs[ch]
            by_el = self.rules_by_element(ch)
            e2f[ch] = {}
            for el in self.elements(ch):
                rules = by_el.get(el, [])
                facts: list[str] = []
                for r in rules:
                    for n in r.inputs:
                        if n not in facts:
                            facts.append(n)
                        ent = f2r.setdefault(n, {"meaning": "", "type": "", "rules": []})
                        ent["rules"].append(f"{ch}/{short_id(r.id)}")
                    rules_idx.append({
                        "id": r.id, "chapter": ch, "element": r.element, "title": r.data["title"], "kind": r.kind,
                        "column": r.column, "coding": r.data.get("coding") or [], "inputs": r.inputs,
                        "fallback": r.fallback, "page": page_of(r.data), "verify": bool(r.data.get("verify")),
                        "path": self.record_path(r, ch)})
                if rules:
                    e2f[ch][el] = {"title": self.element_title(ch, el), "facts": sorted(facts),
                                   "pack": f"elements/{ch}/{el}.md"}
        for n, ent in f2r.items():
            f = None
            chs = [r.split("/")[0] for r in ent["rules"]]
            for ch in chs:
                f = self.vocab.by_chapter.get(ch, {}).get(n)
                if f:
                    break
            if f is None:
                f = self.vocab.get(n, chs[0])
            ent["meaning"] = _ws(f.meaning) if f else ""
            ent["type"] = f.type if f else ""
            ent["rules"] = sorted(set(ent["rules"]), key=lambda s: (CHAPTERS.index(s.split("/")[0]),
                                                                   clause_key(f"rcodes:{VERSION}/{s}")))
        f2r = dict(sorted(f2r.items()))
        self.put("indexes/facts-to-rules.json", _json_lines(f2r))
        md = ["# Facts to rules", "", "Fact name, type and meaning (from the chapter FACTS.md), then the rules that need it, "
              "grouped by chapter. JSON form: `facts-to-rules.json`.", ""]
        for n, ent in f2r.items():
            groups: dict[str, list[str]] = {}
            for s in ent["rules"]:
                c, sid = s.split("/", 1)
                groups.setdefault(c, []).append(sid)
            g = "; ".join(f"{c}: {', '.join(v)}" for c, v in groups.items())
            meaning = f": {ent['meaning'].rstrip('.')}" if ent["meaning"] else ""
            md.append(f"- `{n}` ({ent['type'] or '?'}){meaning}. Rules: {g}")
        self.put("indexes/facts-to-rules.md", "\n".join(md) + "\n")

        self.put("indexes/elements-to-facts.json",
                 "{\n" + ",\n".join(f"{json.dumps(ch)}:" + _json_lines(v).rstrip("\n") for ch, v in e2f.items()) + "\n}\n")
        md = ["# Elements to facts", "", "The facts each element's provisions need. Ask for these before opening "
              "the pack's records. JSON form: `elements-to-facts.json`.", ""]
        for ch in CHAPTERS:
            md += [f"## {self.pkgs[ch].meta['title']}", ""]
            for el, ent in e2f[ch].items():
                md.append(f"- {el} {ent['title']} (`{ent['pack']}`): {_facts_compact(ent['facts'])}")
            md.append("")
        self.put("indexes/elements-to-facts.md", "\n".join(md).rstrip("\n") + "\n")

        body = ",\n".join(json.dumps(o, ensure_ascii=False, separators=(",", ":")) for o in rules_idx)
        self.put("indexes/rules.json", "[\n" + body + "\n]\n")
        self.build_flagged()
        self.build_topics()

    def build_topics(self) -> None:
        L = ["# Topics", "",
             "Subject keyword to rule IDs, by chapter, then element number, then IDs. Element numbers differ between "
             "chapters (element map in `README.md`), so find the subject here, then grep the pack "
             "(`elements/<chapter>/<element>.md`) for the ID. Matched on rule titles only: a provision whose title "
             "does not use the word is missed, so also scan the element's section of the chapter digest.", ""]
        for name, pat in TOPIC_PATTERNS:
            on_element = pat.startswith("element:")
            rx = re.compile(pat.removeprefix("element:"), re.I)
            parts = []
            for ch in CHAPTERS:
                by_el = self.rules_by_element(ch)
                groups = []
                for el in self.elements(ch):
                    if on_element:
                        hit = bool(rx.search(self.element_title(ch, el)))
                        ids = [short_id(r.id) for r in by_el.get(el, [])] if hit else []
                    else:
                        ids = [short_id(r.id) for r in by_el.get(el, []) if rx.search(r.data["title"])]
                    if ids:
                        groups.append(f"{el} " + ", ".join(ids))
                if groups:
                    parts.append(f"{ch}: " + "; ".join(groups))
            if parts:
                L += [f"## {name}", ""] + [f"- {p}" for p in parts] + [""]
        self.put(TOPICS, "\n".join(L).rstrip("\n") + "\n")

    def element_map(self) -> list[str]:
        """README rows: elements whose number differs between chapters (same title, or an ELEMENT_ALIASES title)."""
        cells: dict[str, dict[str, str]] = {}
        for ch in CHAPTERS:
            for el in self.elements(ch):
                t = self.element_title(ch, el)
                key = ELEMENT_ALIASES.get(ch, {}).get(t, t)
                cells.setdefault(key, {})[ch] = el if key == t else f"{el} ({t})"
        rows = []
        for key, c in cells.items():
            if len(c) >= 2 and len({v.split(" ")[0] for v in c.values()}) > 1:
                rows.append(f"| {key} | " + " | ".join(c.get(ch, "-") for ch in CHAPTERS) + " |")
        return rows

    def build_flagged(self) -> None:
        L = ["# Records still flagged", "",
             "Records the page-image verification pass kept flagged `verify`, with the note naming the ambiguity. "
             "Most are inconsistencies in the draft itself, not transcription doubts; quote them as such.", ""]
        total = 0
        for ch in CHAPTERS:
            pkg = self.pkgs[ch]
            recs = sorted([r for r in list(pkg.rules.values()) + list(pkg.fallbacks.values()) if r.data.get("verify")],
                          key=lambda r: (element_key(r.element), clause_key(r.id)))
            tabs = sorted({t["id"]: t for t in pkg.tables.values() if t.get("verify")}.values(), key=lambda t: t["id"])
            excs = [(r, e) for r in sorted(pkg.rules.values(), key=lambda r: (element_key(r.element), clause_key(r.id)))
                    for e in r.exceptions if e.get("verify")]
            total += len(recs) + len(tabs) + len(excs)
            L += [f"## {pkg.meta['title']}", ""]
            if recs:
                L += ["### Rules and fallbacks", ""]
                L += [f"- `{short_id(r.id)}` (p{page_of(r.data)}, `{self.record_path(r, ch)}`): "
                      f"{self.flag_note(r.data) or 'no note'}" for r in recs]
                L.append("")
            if tabs:
                L += ["### Tables", ""]
                L += [f"- `{t['id']}` (p{page_of(t)}): {self.flag_note(t) or 'no note'}" for t in tabs]
                L.append("")
            if excs:
                L += ["### Exceptions", ""]
                L += [f"- `{short_id(r.id)}` exception \"{_ws(e.get('label'))}\"" +
                      (f" ({_ws(e['source'])})" if e.get("source") else "") +
                      (f": {_ws(e['note'])}" if e.get("note") else "") for r, e in excs]
                L.append("")
        a1 = [t for t in self.a1_doc["terms"] if t.get("verify")]
        if a1:
            L += ["## Appendix A1 definitions", ""]
            L += [f"- *{t['term']}* (p{t.get('page', '')}): {_ws(t.get('note') or self.flag_note(t)) or 'no note'}"
                  for t in a1]
            total += len(a1)
        self.flagged_total = total
        self.put("indexes/flagged.md", "\n".join(L).rstrip("\n") + "\n")

    # entry layer ---------------------------------------------------------------------
    def build_entry(self) -> None:
        v = self.reg.version(VERSION)
        n_rules = sum(len(p.rules) for p in self.pkgs.values())
        n_fb = sum(len(p.fallbacks) for p in self.pkgs.values())
        n_tab = sum(len({t["id"] for t in p.tables.values()}) for p in self.pkgs.values())
        recs = [r for p in self.pkgs.values() for r in list(p.rules.values()) + list(p.fallbacks.values())]
        n_stamped = sum(1 for r in recs if r.data.get("verified"))
        n_flag = sum(1 for r in recs if r.data.get("verify"))
        t11 = []
        for row in self.t11["rows"]:
            ch = row.get("chapter")
            t11.append(f"| {row['dwelling_type'].replace('_', ' ')} | {', '.join(row['coding'])} | "
                       f"{ch or 'none (not provided for)'} | {row.get('pathway') or '-'} |")
        digests = "\n".join(f"| `chapters/{ch}/digest.md` | {self.pkgs[ch].meta['title']} | {len(self.pkgs[ch].rules)} | "
                            f"~{tokens(self.files[f'chapters/{ch}/digest.md'])} |" for ch in CHAPTERS)
        dsz = sorted(tokens(self.files[f"chapters/{ch}/digest.md"]) for ch in CHAPTERS)
        psz = sorted(tokens(v) for k, v in self.files.items() if k.startswith("elements/"))
        rsz = sorted(tokens(v) for k, v in self.files.items() if re.match(r"records/ch[^/]+/rules/", k))
        ch1_files = [CH1_OPERATION] + ([CH1_PERMISSIONS] if CH1_PERMISSIONS in self.files else [])
        ch1_sizes = ", ".join(f"`{p}` ~{tokens(self.files[p])}" for p in ch1_files)
        lv_pointer = LOCAL_VARIATION_POINTER.format(perm=ch1_files[-1], op=CH1_OPERATION)
        ex = re.search(r"^- `C3\.3\.3` .*$", self.files["chapters/ch2/digest.md"].decode("utf-8"), re.M)
        digest_example = f"    {ex.group(0)[2:]}" if ex else ""
        readme = f"""# Draft WA Residential Design Codes: machine-readable edition

This directory is the generated recall layer of a machine-readable edition of the **draft consolidated
Residential Design Codes (R-Codes)** of Western Australia, version `{VERSION}`: advertised
{_long_date(v['date'])}, consultation closes {_long_date(v.get('consultation_closes', ''))}. It is a draft
under consultation, not the code in force; values will be re-derived at gazettal. Every file here except
`{SKILL}`, `{GOVERNANCE}`, `worked/`, `graph/` and `schema/` is generated by `python -m rcodes publish` from the JSON records; do not edit
it by hand. To assess a plan, follow `{SKILL}` (skill `rcodes-draft-assessment`: run the Python engine, or apply
the edition by hand; one report format for both).

## What it contains, and what it does not

Contains: every provision of Chapters 2, 3, 4 Part 1 and 4 Part 2 as a structured record with a stable ID,
printed text, source page and encoded test ({n_rules} provisions, {n_fb} merit, objective and design-guidance
records, {n_tab} tables); the Chapter 1 operation layer (Table 1.1 applicability, Figure 2.1 development
applications, Table 2.4 consultation, local variation by LPP and LDP under Tables 2.5A, 2.5B and 3.5A, clause
2.5.2); Appendix A1 definitions.

Does not contain: the R-Codes currently in force; any local instrument (scheme, local planning policy, local
development plan, structure plan) or its variations, only the rules on what they may vary; a spatial layer (lot
boundaries, R-coding maps, Location A or B, Perth and Peel extents); plan reading (facts are supplied by a
person or another tool and tested here).

## How to read it

Search, do not read whole files: read the digest's element headings, then grep the element packs for a clause
ID (``^### `C3.3.1` ``) and read only the matching section.

1. Pick the chapter from Table 1.1 below.
2. Scan that chapter's digest headings (`## <element> <title> (coding ...; fb <fallback>)`); each line under
   one is a provision (format below). To find a subject across chapters, use `{TOPICS}`.
3. Grep the element pack for the clause ID. Under each `### ` heading the first line lists the facts the
   provision needs; stop there if that is all you need, else read on for the printed text, test, tables and
   exceptions.
4. {lv_pointer}

Digest line, fields split by `;`: `` `ID` title``; kind (`m` measurable, `c` conditional, `j` judgment, with
`/M`, `/O` or `/DG` when not in the testable column); coding (`=` same as the heading); facts (one or two
named, else the count and the first two; `site.r_code` is never counted); test (`>=`/`<=` a value, `yes`/`no`,
a table looked up by coding unless `by <fact>`, `all(...)`/`any(...)` for several tests); `exc n: labels`
(exceptions, tried in order); `fb ID` (a fallback other than the element's); ⚑ (flagged verify). Example (ch2):

{digest_example}

| Layer | Path | Use | Size (tokens) |
|---|---|---|---|
| entry | `README.md` | this file | ~{{tokens_placeholder}} |
| chapter 1 | `chapters/ch1/` | operation: applicability, DA, consultation, LPP and LDP permission levels | {ch1_sizes} |
| digest | `chapters/<ch>/digest.md` | one line per provision: ID, title, kind, coding, facts, test, exceptions, fallback | {dsz[0]}-{dsz[-1]} |
| pack | `elements/<ch>/<element>.md` | one element in full: local variation, merit or objectives, questions, provisions | {psz[0]}-{psz[-1]}, median {psz[len(psz) // 2]} |
| index | `indexes/` | `facts-to-rules`, `elements-to-facts`, `topics` (subject to IDs), `rules.json`, `flagged.md` | per entry |
| definitions | `definitions/A1.md`, `A1.json` | Appendix A1, 197 terms; grep the term | per term |
| records | `records/<ch>/` | exact JSON (rules, fallbacks, tables; ch1 data) | rule median ~{rsz[len(rsz) // 2] if rsz else 0} |

| Digest | Chapter | Provisions | Tokens |
|---|---|---|---|
{digests}

`graph/` (JSON-LD) and `schema/` (application schema) come from a separate export. `llms.txt` lists every file.
Clause IDs: `rcodes:{VERSION}/<chapter>/<clause>[#fragment]`; digests and packs use the short form
(`C3.3.1#laneway`).

## Which chapter (Chapter 1, Table 1.1)

| Dwelling type | Coding | Chapter | Pathway |
|---|---|---|---|
{chr(10).join(t11)}

Chapter 1A operates Chapters 2, 3 and 4 Part 1; Chapter 1B operates Chapter 4 Part 2. Mixed use: the
dwellings are multiple dwellings. Printed text, Figure 2.1 and Table 2.4: `{CH1_OPERATION}`.

**Element numbers differ between chapters.** 3.3 is street setbacks in ch2, ch3 and ch4p1 but tree canopy and
deep soil areas in ch4p2; solar access for adjoining sites and visual privacy are 3.9 and 3.10 in ch2 and ch3,
3.8 and 3.9 in ch4p1. Always cite chapter with clause. Where the number differs:

| Element | ch2 | ch3 | ch4p1 | ch4p2 |
|---|---|---|---|---|
{chr(10).join(self.element_map())}

**Location A and B** (parking) are defined in the note to Table 2.3a: Location A is land within 800 m of a
train station on a high-frequency rail route, within 250 m of a high-frequency transit route, or within an
activity centre; Location B is all other land. Record: `records/ch2/tables/table-2.3a.json` (`notes`, Chapter 2
p18; same note in `ch3` and `ch4p1` `tables/table-2.3a.json`, and Chapter 4 Part 2
`records/ch4p2/tables/table-3.9-resident.json`). The edition cannot tell which applies to a lot; ask.

## Assessment procedure

In full, with the report format, in `{SKILL}`. In short: pick the chapter (Table 1.1); choose the elements the
plan engages (a single house touches about eight); collect each pack's facts and ask for any not given; filter
provisions by coding, dwelling type, region and "Applies only when"; evaluate each test, trying exceptions in
order; report status, clause ID, page and the value against the threshold; for anything not met, name the
fallback (M, or O informed by DG). Open `records/` when an exact value matters; run the engine
(`python -m rcodes run`) where Python is available.
Worked example (a two-storey project home design on a 15 m x 30 m R20 lot, plan-only and with a declared siting): `{WORKED}`.

## How statuses read

- **meets** / **does not meet**: the encoded test ran on supplied facts.
- **cannot tell**: a needed fact is missing or below confidence; name the fact and ask for it.
- **not applicable**: the provision's coding, type or conditions exclude the case, or the table has no provision.
- **not evaluated**: a judgment provision with no encoded test; assess it against its text.
- **Deemed exempt** (Chapters 2, 3, 4 Part 1): meeting every applicable C provision; a C not met goes to
  **merit** assessment against the element's M record. **Performance** (Chapter 4 Part 2): the A acceptable
  outcomes; an A not met is assessed against the element objectives (O), informed by design guidance (DG).

## Honesty rules

- Never guess a missing fact and never apply a default to one; report cannot tell and name the fact.
- Cite every finding by clause ID and source page; quote the printed text where it decides the matter.
- A record marked ⚑ (`verify: true`) carries an ambiguity in the draft itself, named in its note; report it
  with the finding rather than resolving it silently. See `indexes/flagged.md`.
- Only the records are authoritative; digests and packs are summaries generated from them.

## Verification state

{n_stamped} of {len(recs)} rule and fallback records carry a `verified` stamp: every value and text was
checked against the page image in one pass by an AI model (Claude Opus 4.5, 2 November 2026,
`opus-4.5-pass-1`), with two value corrections. No human review yet; corrections welcome by issue.
{n_flag} records remain flagged where the page itself is ambiguous; {self.flagged_total} flagged items in all
(records, tables, exceptions, A1 terms) are in `indexes/flagged.md`. Corrections and confirmed draft inconsistencies are
logged in the repository's `CHANGELOG.md` (`../CHANGELOG.md`). What governs, versions, citation, error reports
and the disclaimer: `{GOVERNANCE}`. Plain-English guide: `../HOW-TO-USE.md`.
"""
        readme = readme.replace("~{tokens_placeholder}", "~" + str(tokens(readme) + 1))
        self.put("README.md", readme)
        self.put("CLAUDE.md", f"""# Claude Code instructions for this edition

Read `README.md` in this directory first and follow it. It tells you which chapter applies (Table 1.1), the
order to read the layers (digest, then element packs, then indexes and records) and the assessment procedure.
To assess a plan, follow `{SKILL}`.

- Do not read the whole directory. Open one chapter digest, then grep the element packs for clause IDs
  (``^### `C3.3.1` ``) and read only the matching section. Element numbers differ between chapters; find a
  subject in `{TOPICS}`.
- {lv_pointer}
- Never guess a missing fact; report cannot tell and name it.
- Cite clause IDs (`rcodes:{VERSION}/<chapter>/<clause>`) and source pages for every finding.
- Records marked ⚑ carry the draft's own ambiguity; say so. See `indexes/flagged.md`.
- The PDF governs; this edition is unofficial and not planning advice. See `{GOVERNANCE}`.
- Files here other than `{SKILL}`, `{GOVERNANCE}`, `worked/`, `graph/` and `schema/` are generated
  (`python -m rcodes publish`); edit the records under `src/`, not this directory.
""")
        L = [f"# Draft WA Residential Design Codes ({VERSION}), machine-readable edition", "",
             f"> Every provision of the draft consolidated R-Codes (advertised {_long_date(v['date'])}, consultation "
             f"closes {_long_date(v.get('consultation_closes', ''))}) as a structured record with stable ID, printed "
             "text, source page and encoded test, with chapter digests and element packs sized for a model to "
             "assess a plan within a small token budget.", "",
             "Start with README.md. Select the chapter by Table 1.1, read its digest, then open element packs.", "",
             "## Entry", "", "- [README](README.md): what this is, chapter selection, assessment procedure, statuses",
             "- [CLAUDE.md](CLAUDE.md): instructions for Claude Code",
             f"- [SKILL.md]({SKILL}): assessment skill (rcodes-draft-assessment): procedure, both modes, report format",
             f"- [GOVERNANCE.md]({GOVERNANCE}): what governs, versions, verification, citation, corrections, disclaimer",
             "- [HOW-TO-USE.md](../HOW-TO-USE.md): plain-English guide for non-developers (repository root)",
             f"- [Worked example]({WORKED}): a two-storey, 5-bedroom project home design on a 15 m x 30 m R20 lot, plan-only and with a declared siting",
             "", "## Chapter 1 operation", "",
             f"- [Operation]({CH1_OPERATION}): Table 1.1, Figure 2.1, Table 2.4, LPP and LDP variation, clause 2.5.2"]
        if CH1_PERMISSIONS in self.files:
            L.append(f"- [Permissions]({CH1_PERMISSIONS}): per element, what an LPP and an LDP may vary and at what level")
        L += ["", "## Digests", ""]
        L += [f"- [{self.pkgs[ch].meta['title']}](chapters/{ch}/digest.md): one line per provision" for ch in CHAPTERS]
        L += ["", "## Indexes", "",
              "- [Facts to rules](indexes/facts-to-rules.md) ([JSON](indexes/facts-to-rules.json))",
              "- [Elements to facts](indexes/elements-to-facts.md) ([JSON](indexes/elements-to-facts.json))",
              f"- [Topics]({TOPICS}): subject keyword to rule IDs across chapters",
              "- [Rules](indexes/rules.json): every rule, compact, with record path",
              "- [Flagged records](indexes/flagged.md): records still flagged verify, with notes",
              "", "## Definitions", "",
              "- [Appendix A1](definitions/A1.md) ([JSON](definitions/A1.json))", ""]
        for ch in CHAPTERS:
            L += [f"## Element packs: {self.pkgs[ch].meta['title']}", ""]
            for el in self.elements(ch):
                rel = f"elements/{ch}/{el}.md"
                if rel in self.files:
                    L.append(f"- [{el} {self.element_title(ch, el)}]({rel})")
            L.append("")
        L += ["## Optional", "", "- [Records](records/): exact JSON records per chapter (rules, fallbacks, tables)"]
        self.put("llms.txt", "\n".join(L) + "\n")

    # writing -----------------------------------------------------------------------
    def check_placement(self) -> None:
        """Every rule in one digest line and one pack; every fallback in one pack."""
        for ch in CHAPTERS:
            pkg = self.pkgs[ch]
            digest = self.files[f"chapters/{ch}/digest.md"].decode("utf-8")
            dl = re.findall(r"^- `([^`]+)`", digest, re.M)
            packs = "".join(self.files[k].decode("utf-8") for k in sorted(self.files)
                            if k.startswith(f"elements/{ch}/"))
            ph = re.findall(r"^### `([^`]+)`", packs, re.M)
            fh = re.findall(r"^## (?:Merit assessment|Element objectives|Design guidance) `([^`]+)`", packs, re.M)
            for r in pkg.rules.values():
                s = short_id(r.id)
                if dl.count(s) != 1 or ph.count(s) != 1:
                    self.unplaced.append(f"{r.id}: digest {dl.count(s)}, pack {ph.count(s)}")
            for f in pkg.fallbacks.values():
                s = short_id(f.id)
                if fh.count(s) != 1:
                    self.unplaced.append(f"{f.id}: pack {fh.count(s)} (column {f.column})")

    def write(self) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        for d in MANAGED_DIRS:
            if (self.out / d).exists():
                shutil.rmtree(self.out / d)
        for rel, data in sorted(self.files.items()):
            p = self.out / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(lf(data))


def _collapse(codes: set[str]) -> str:
    """{'R30','R35',...,'R160','LR'} -> 'R30+,LR'; contiguous numeric runs become ranges."""
    nums = [c for c in codings.NUMERIC if c in codes]
    out: list[str] = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and codings.NUMERIC.index(nums[j + 1]) == codings.NUMERIC.index(nums[j]) + 1:
            j += 1
        a, b = nums[i], nums[j]
        if a == b:
            out.append(a)
        elif b == codings.NUMERIC[-1]:
            out.append(f"{a}+")
        else:
            out.append(f"{a}-{b}")
        i = j + 1
    out += [c for c in codings.NAMED if c in codes]
    return ",".join(out)


def _rounding_words(text: str) -> str:
    """Put the rounding rule in words beside each `round(... + 0.001)` style call (ROUNDING_WORDS)."""
    out: list[str] = []
    i = 0
    while True:
        j = text.find("round(", i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        depth, k = 0, j + 5
        while k < len(text):
            depth += {"(": 1, ")": -1}.get(text[k], 0)
            if depth == 0:
                break
            k += 1
        if k >= len(text):
            out.append(text[i:])
            return "".join(out)
        call = text[j:k + 1]
        out.append(text[i:k + 1])
        for tail, words in ROUNDING_WORDS:
            if call.endswith(tail) and not text.startswith(f" ({words})", k + 1):
                out.append(f" ({words})")
                break
        i = k + 1


def _json_lines(d: dict[str, Any]) -> str:
    """A JSON object with one compact member per line: small, greppable and diff-friendly."""
    body = ",\n".join(f"{json.dumps(k, ensure_ascii=False)}:{json.dumps(v, ensure_ascii=False, separators=(',', ':'))}"
                      for k, v in d.items())
    return "{\n" + body + "\n}\n"


def _facts_compact(names: list[str], sep: str = ", ") -> str:
    """['site.r_code', 'site.has_row', 'building.x'] -> 'site.{r_code,has_row}, building.x'"""
    groups: dict[str, list[str]] = {}
    for n in names:
        pre, _, leaf = n.rpartition(".")
        groups.setdefault(pre, []).append(leaf)
    out = []
    for pre, leaves in groups.items():
        if not pre:
            out += leaves
        elif len(leaves) == 1:
            out.append(f"{pre}.{leaves[0]}")
        else:
            out.append(f"{pre}.{{{','.join(leaves)}}}")
    return sep.join(out)


def _short_words(text: str, n: int) -> str:
    """Shorten to at most about n characters, cutting only at a space (never mid-word)."""
    t = _ws(text)
    if len(t) <= n:
        return t
    cut = t[:n + 1].rsplit(" ", 1)[0].rstrip(" ,;:(&-")
    return (cut or t.split(" ", 1)[0]) + " …"


TITLE_CHARS = 44  # digest title length before the region suffix; cut at a word boundary

_REGION_SUFFIX = {"perth-peel": ("Perth and Peel", ("perth and peel",)),
                  "regional": ("regional", ())}


def _digest_title(title: str, region: str | None, keep_paren: bool = False) -> str:
    """Digest form of a title: full words, no articles; a long title drops its trailing parenthetical (the
    value is in the test field) and is cut at a word boundary. The region is taken out before the cut and
    put back after it, so regional variants stay distinguishable."""
    t = _ws(title)
    if len(t) > 40 and not keep_paren:
        t = re.sub(r"\s*\([^()]*\)$", "", t).strip() or t
    label = None
    if region in _REGION_SUFFIX:
        label = _REGION_SUFFIX[region][0]
        t = re.sub(r",?\s*(?:outside|within|in)?\s*(?:the\s+)?Perth and Peel(?: regions?)?", "", t, flags=re.I).strip(" ,")
        t = re.sub(r",?\s*regional", "", t, flags=re.I).strip(" ,") or _ws(title)
    t = re.sub(r"(?<![\w-])(the|a|an) (?=\w)", "", t, flags=re.I)
    t = _short_words(t[:1].upper() + t[1:], TITLE_CHARS + (24 if keep_paren else 0))
    if t.count("(") > t.count(")"):
        t = t[:t.rindex("(")].rstrip(" ,;:") + " …"
    if label:
        t += f", {label}"
    return t.replace(";", ",")


def _distinct_titles(rules: list[Rule], coding_of) -> dict[str, str]:
    """Digest titles for an element's rules, made distinct: a title shared by two rules keeps its
    parenthetical, then gets the region, then the coding, then the dwelling types, then the clause ID appended until it is unique."""
    out = {r.id: _digest_title(r.data["title"], r.data.get("region")) for r in rules}
    scopes = [
        lambda r: _digest_title(r.data["title"], r.data.get("region"), keep_paren=True),
        lambda r: {"perth-peel": "Perth and Peel", "regional": "regional"}.get(r.data.get("region") or "", ""),
        lambda r: coding_of(r),
        lambda r: ", ".join(t.replace("_", " ") for t in r.data.get("applies_to") or []),
        lambda r: short_id(r.id),
    ]
    for scope in scopes:
        seen: dict[str, list[Rule]] = {}
        for r in rules:
            seen.setdefault(out[r.id].lower(), []).append(r)
        dups = [g for g in seen.values() if len(g) > 1]
        if not dups:
            break
        for g in dups:
            labels = [scope(r) for r in g]
            if len(set(labels)) == 1:
                continue
            if scope is scopes[0]:
                for r, lab in zip(g, labels):
                    out[r.id] = lab
                continue
            for r, lab in zip(g, labels):
                if lab and lab.lower() not in out[r.id].lower():
                    out[r.id] += f", {lab}"
    return out


def _facts_count(names: list[str]) -> str:
    """Digest facts field: up to two names in full (a shared prefix braced); more becomes
    'n facts: first, second' with the full list under the provision's heading in the pack."""
    if not names:
        return "-"
    shown = _facts_compact(names[:2])
    return shown if len(names) <= 2 else f"{len(names)} facts: {shown}"


def _exc_tag(e: dict[str, Any]) -> str:
    """Digest form of an exception label: its leading clause reference, else a short label."""
    label = _ws(e.get("label"))
    m = re.match(r"^((?:[CAMO]|DG)\d+\.\d+(?:\.\d+)?(?:\([ivx]+\))?)\b", label)
    return m.group(1) if m else _short_words(_exc_label(e), 18)


def _exc_label(e: dict[str, Any]) -> str:
    label = _ws(e.get("label"))
    return re.split(r"[:;(]", label, maxsplit=1)[0].strip() or label


_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"]


def _long_date(iso: str) -> str:
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})$", iso or "")
    if not m:
        return iso or "unknown"
    return f"{int(m[3])} {_MONTHS[int(m[2]) - 1]} {m[1]}"


def generate(reg: Registry | None = None, out: Path | None = None) -> Edition:
    """Build the edition in memory (Edition.files) without writing it."""
    reg = reg or Registry.load(strict=False)
    ed = Edition(reg=reg, out=Path(out) if out else REPO_ROOT / "edition")
    ed.build()
    ed.check_placement()
    return ed


def sizes(ed: Edition) -> dict[str, int]:
    return {rel: tokens(data) for rel, data in ed.files.items() if not rel.startswith("records/")}


def publish(reg: Registry | None = None, out: Path | None = None) -> Edition:
    ed = generate(reg, out)
    ed.write()
    return ed


def report(ed: Edition) -> str:
    sz = sizes(ed)
    lines = [f"edition written to {ed.out}", f"{len(ed.files)} files"]
    for rel in ("README.md", "CLAUDE.md", "llms.txt"):
        lines.append(f"  {rel}: {sz[rel]} tokens")
    for rel in (CH1_OPERATION, CH1_PERMISSIONS):
        if rel in sz:
            lines.append(f"  {rel}: {sz[rel]} tokens")
    for ch in CHAPTERS:
        lines.append(f"  chapters/{ch}/digest.md: {sz[f'chapters/{ch}/digest.md']} tokens")
    packs = sorted((v, k) for k, v in sz.items() if k.startswith("elements/"))
    if packs:
        lines.append(f"  element packs: {len(packs)}; smallest {packs[0][0]} ({packs[0][1]}); median "
                     f"{packs[len(packs) // 2][0]}; largest {packs[-1][0]} ({packs[-1][1]}); over "
                     f"{PACK_TARGET_TOKENS[1]}: {sum(1 for v, _ in packs if v > PACK_TARGET_TOKENS[1])}")
    for rel in sorted(k for k in sz if k.startswith(("indexes/", "definitions/"))):
        lines.append(f"  {rel}: {sz[rel]} tokens")
    lines.append(f"unplaced: {len(ed.unplaced)}")
    lines += [f"  {u}" for u in ed.unplaced]
    lines.append(f"facts with no FACTS.md entry: {len(ed.vocab.unknown)}")
    lines.append(f"defined terms with no A1 entry: {len(ed.defs.missing)}")
    return "\n".join(lines)
