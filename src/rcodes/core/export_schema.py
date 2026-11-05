"""Consolidated application data schema, generated from the chapter fact vocabularies.

    python -m rcodes.core.export_schema --out edition/schema

Reads every src/rcodes/chapters/*/FACTS.md (Markdown tables: fact, type, meaning, plus
usage-note bullets) and the base core/schemas/application.schema.json, and writes

    application.schema.json   one JSON Schema; dotted fact names become nested objects
    application.md            the same, rendered as Markdown tables

Each fact property carries its meaning as description, x-used-by (the rule and fallback
IDs whose inputs, evaluator, conditions or exceptions read it), x-vocabulary (the
chapters whose FACTS.md lists it) and x-notes (usage notes naming it). Facts read by
rules but absent from every FACTS.md are added with x-undocumented: true and no type.

Facts that are null mean unknown (core/facts.py), so every leaf typed from a FACTS.md row also
admits null; leaves already typed in the base schema keep the base type unchanged.
The output is deterministic: rerunning on unchanged inputs gives byte-identical files.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any, Iterable

from . import codings
from .registry import PKG_ROOT, Registry
from .rules import Rule

CHAPTERS_DIR = PKG_ROOT / "chapters"
BASE_SCHEMA = Path(__file__).parent / "schemas" / "application.schema.json"
INSTRUMENT_SCHEMA = Path(__file__).parent / "schemas" / "instrument.schema.json"
SCHEMA_ID = "https://riseurban.au/rcodes/edition/schema/application.schema.json"
VOCAB_ORDER = ["ch2", "ch3", "ch4p1", "ch4p2"]

FACT_RE = re.compile(r"(?<![\w.])[a-z_][a-z0-9_]*(?:\.(?:[a-z0-9_]+|<[a-z_]+>|\*))+")
_ENUM_TOKEN = re.compile(r"^[A-Za-z0-9_+-]+$")


# --- fact vocabularies -------------------------------------------------------------

def parse_facts_md(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Rows (name, type, meaning, section) and usage-note bullets (text, section)."""
    rows: list[dict[str, Any]] = []
    notes: list[dict[str, Any]] = []
    section = ""
    last_note: dict[str, Any] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            last_note = None
            continue
        if line.startswith("|"):
            last_note = None
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= {"-", ":", " "} or cells[0].lower() == "fact":
                continue
            ftype, meaning = cells[1], " | ".join(cells[2:]).strip()
            for name in cells[0].split(","):
                name = name.strip().strip("`").strip()
                if name:
                    rows.append({"name": name, "type": ftype, "meaning": meaning, "section": section})
            continue
        if line.startswith("- "):
            last_note = {"text": line[2:].strip(), "section": section}
            notes.append(last_note)
        elif line.strip() and last_note is not None and raw.startswith(" "):
            last_note["text"] += " " + line.strip()
        elif not line.strip():
            last_note = None
    return rows, notes


def load_vocabularies(chapters_dir: Path = CHAPTERS_DIR) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Merged vocabulary {name: {type, types, meaning, vocab, section}} and deduplicated notes."""
    facts: dict[str, dict[str, Any]] = {}
    notes: list[dict[str, Any]] = []
    seen_notes: set[str] = set()
    for ch in VOCAB_ORDER:
        path = chapters_dir / ch / "FACTS.md"
        if not path.exists():
            continue
        rows, nts = parse_facts_md(path)
        for r in rows:
            f = facts.setdefault(r["name"], {"types": [], "meanings": [], "vocab": [], "section": r["section"]})
            if r["type"] not in f["types"]:
                f["types"].append(r["type"])
            if r["meaning"] and r["meaning"] not in f["meanings"]:
                f["meanings"].append(r["meaning"])
            if ch not in f["vocab"]:
                f["vocab"].append(ch)
        for n in nts:
            if n["text"] not in seen_notes:
                seen_notes.add(n["text"])
                notes.append(n)
    return facts, notes


def note_targets(text: str, known: Iterable[str]) -> list[str]:
    """Fact names a usage note is about: the dotted names before its first ': '."""
    known = list(known)
    head = text.split(": ", 1)[0] if ": " in text else ""
    out: list[str] = []
    for tok in FACT_RE.findall(head):
        if tok.endswith(".*"):
            out += [k for k in known if k.startswith(tok[:-1])]
        elif tok in known:
            out.append(tok)
    return sorted(dict.fromkeys(out))


# --- what rules read ---------------------------------------------------------------

def _walk_facts(node: Any, out: set[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("fact", "of") and isinstance(v, str):
                out.add(v.strip())
            elif k == "inputs" and isinstance(v, list):
                out.update(x.strip() for x in v if isinstance(x, str))
            elif k in ("expr", "value") and isinstance(v, str):
                out.update(FACT_RE.findall(v))
            else:
                _walk_facts(v, out)
    elif isinstance(node, list):
        for x in node:
            _walk_facts(x, out)


def rule_facts(rule: Rule) -> list[str]:
    """Facts a record reads: inputs plus evaluator, condition and exception facts."""
    out: set[str] = set(x.strip() for x in rule.inputs)
    for key in ("evaluator", "conditions", "exceptions"):
        _walk_facts(rule.data.get(key), out)
    return sorted(f for f in out if "." in f)


def used_by(registry: Registry) -> dict[str, list[str]]:
    index: dict[str, set[str]] = {}
    for rec in registry.all_rules() + registry.all_fallbacks():
        for f in rule_facts(rec):
            index.setdefault(f, set()).add(rec.id)
    return {k: sorted(v) for k, v in sorted(index.items())}


def pattern_match(pattern: str, name: str) -> bool:
    rx = "^" + re.escape(pattern).replace(re.escape("<type>"), r"[a-z0-9_]+") + "$"
    return re.match(rx, name) is not None


# --- schema construction -----------------------------------------------------------

def _enum_values(ftype: str, meaning: str) -> list[str] | None:
    if " / " in ftype:
        vals = [v.strip() for v in ftype.split(" / ")]
        return vals if all(_ENUM_TOKEN.match(v) for v in vals) else None
    if ftype == "enum":
        head = re.split(r"[(;]", meaning, maxsplit=1)[0]
        vals = [v.strip() for v in head.split(",") if v.strip()]
        if len(vals) >= 2 and all(_ENUM_TOKEN.match(v) for v in vals):
            return vals
        return None
    if _ENUM_TOKEN.match(ftype) and ftype not in ("number", "int", "bool", "code", "list", "enum", "polygon"):
        return [ftype]
    return None


def type_schema(types: list[str], meaning: str) -> dict[str, Any]:
    """JSON Schema for a fact's type column (several columns merge as a union)."""
    enums: list[str] = []
    kinds: list[str] = []
    out: dict[str, Any] = {}
    for t in types:
        vals = _enum_values(t, meaning)
        if vals is not None:
            enums += [v for v in vals if v not in enums]
        elif t == "number":
            kinds.append("number")
        elif t == "int":
            kinds.append("integer")
        elif t == "bool":
            kinds.append("boolean")
        elif t in ("code", "enum"):
            kinds.append("string")
            if t == "code":
                out["examples"] = codings.NUMERIC + codings.NAMED
        elif t == "list":
            kinds.append("array")
        elif t == "polygon":
            out["$ref"] = "#/$defs/geometry"
        else:
            kinds.append("string")
    if "number" in kinds and "integer" in kinds:
        kinds.remove("integer")
    if enums and not kinds:
        out["enum"] = enums + [None]
    elif kinds:
        out["type"] = sorted(set(kinds), key=kinds.index) + ["null"]
        if enums:
            out["examples"] = enums
    return out


def _ensure_object(node: dict[str, Any]) -> dict[str, Any]:
    """The object schema under which child properties go (dwellings: the object branch)."""
    if "oneOf" in node:
        for branch in node["oneOf"]:
            if branch.get("type") == "object":
                return _ensure_object(branch)
    if "type" in node and node["type"] != "object":
        leaf = {k: node.pop(k) for k in list(node) if k not in ("description",)}
        node["anyOf"] = [leaf, {"type": "object"}]
        return _ensure_object(node["anyOf"][1])
    if "anyOf" in node:
        for branch in node["anyOf"]:
            if branch.get("type") == "object":
                return _ensure_object(branch)
    node.setdefault("type", "object")
    return node


def _child(parent: dict[str, Any], seg: str) -> dict[str, Any]:
    obj = _ensure_object(parent)
    if seg.startswith("<") and seg.endswith(">"):
        add = obj.get("additionalProperties")
        if not isinstance(add, dict):
            add = obj["additionalProperties"] = {"type": "object", "x-key": seg.strip("<>")}
        return add
    return obj.setdefault("properties", {}).setdefault(seg, {})


def build_schema(registry: Registry, chapters_dir: Path = CHAPTERS_DIR) -> tuple[dict[str, Any], dict[str, Any]]:
    """The schema and a report (counts, undocumented facts, notes not tied to a fact)."""
    base = json.loads(BASE_SCHEMA.read_text(encoding="utf-8"))
    inst = json.loads(INSTRUMENT_SCHEMA.read_text(encoding="utf-8"))
    vocab, notes = load_vocabularies(chapters_dir)
    users = used_by(registry)

    schema = copy.deepcopy(base)
    schema["$id"] = SCHEMA_ID
    schema["title"] = "R-Codes application data document (consolidated, draft-2026-10-24)"
    schema["description"] = (
        "Facts a proposal supplies as data, generated from the base application schema and the fact "
        "vocabularies of Chapters 2, 3, 4 Part 1 and 4 Part 2 (FACTS.md). Property paths are the dotted "
        "fact names rules read (site.verge.path_or_road_offset_m is site -> verge -> path_or_road_offset_m). "
        "A fact that is absent or null is unknown, never zero; every numeric fact should have a facts_meta "
        "entry keyed by its dotted name. dwellings is either an array of per-dwelling objects (flattened as "
        "dwellings.0.bedrooms, with dwellings.count) or an object of development-wide summary facts that "
        "describe the least compliant dwelling or a share of dwellings (dwellings.min.*, dwellings.max.*, "
        "dwellings.*_pct; Chapter 4 Part 1 and Part 2 apartments). x-used-by lists the rule IDs that read a "
        "fact; x-vocabulary the chapters whose FACTS.md lists it. Objects are open: properties not listed "
        "here are allowed."
    )
    schema["x-generated-from"] = ["src/rcodes/core/schemas/application.schema.json"] + [
        f"src/rcodes/chapters/{ch}/FACTS.md" for ch in VOCAB_ORDER if (chapters_dir / ch / "FACTS.md").exists()]
    inst_def = {k: v for k, v in inst.items() if k not in ("$schema", "$id")}
    schema["$defs"] = dict(schema.get("$defs", {}), instrument=inst_def)
    inst_ref = schema["properties"]["site"]["properties"]["instruments"]
    inst_ref["items"] = {"$ref": "#/$defs/instrument"}

    patterns = [n for n in vocab if "<" in n]
    names = list(vocab)
    undocumented = [f for f in users if f not in vocab and not any(pattern_match(p, f) for p in patterns)]
    note_map: dict[str, list[str]] = {}
    loose_notes: list[str] = []
    for n in notes:
        targets = note_targets(n["text"], names)
        for t in targets:
            note_map.setdefault(t, []).append(n["text"])
        if not targets:
            loose_notes.append(n["text"])

    for name in names + undocumented:
        node: dict[str, Any] = schema
        for seg in name.split("."):
            node = _child(node, seg)
        info = vocab.get(name)
        if info is None:
            node.setdefault("description", "read by rules; not listed in any FACTS.md")
            node["x-undocumented"] = True
        else:
            meaning = "; ".join(info["meanings"])
            had_type = any(k in node for k in ("type", "enum", "$ref", "oneOf", "anyOf"))
            if not had_type:
                node.update(type_schema(info["types"], meaning))
            elif "$ref" not in node and "items" not in node and "oneOf" not in node:
                gen = type_schema(info["types"], meaning)
                if node.get("type") in ("string", ["string", "null"]) and "enum" in gen:
                    node.setdefault("examples", [v for v in gen["enum"] if v is not None])
                elif "examples" in gen:
                    node.setdefault("examples", gen["examples"])
            if meaning and "description" not in node:
                node["description"] = meaning
            node["x-type"] = " | ".join(info["types"])
            node["x-vocabulary"] = info["vocab"]
        readers = sorted({r for f, rs in users.items() if f == name or ("<" in name and pattern_match(name, f))
                          for r in rs})
        if readers:
            node["x-used-by"] = readers
        if name in note_map:
            node["x-notes"] = note_map[name]
    if loose_notes:
        schema["x-usage-notes"] = loose_notes
    report = {"facts": len(names), "patterns": len(patterns), "undocumented": undocumented,
              "notes": len(notes), "loose_notes": len(loose_notes),
              "used_facts": len(users)}
    return schema, report



# --- Markdown rendering ------------------------------------------------------------

def _leaves(node: dict[str, Any], prefix: str = "") -> Iterable[tuple[str, dict[str, Any]]]:
    props: dict[str, Any] = {}
    for holder in [node] + node.get("oneOf", []) + node.get("anyOf", []):
        props.update(holder.get("properties", {}))
        add = holder.get("additionalProperties")
        if isinstance(add, dict) and "x-key" in add:
            props[f"<{add['x-key']}>"] = add
    if "x-type" in node or "x-undocumented" in node:
        yield prefix, node
    for k, v in props.items():
        if prefix == "" and k == "facts_meta":
            continue
        yield from _leaves(v, f"{prefix}.{k}" if prefix else k)


def _type_label(node: dict[str, Any]) -> str:
    if "enum" in node:
        return " / ".join(str(v) for v in node["enum"] if v is not None)
    for holder in [node] + node.get("anyOf", []):
        t = holder.get("type")
        if t:
            t = [x for x in (t if isinstance(t, list) else [t]) if x != "null"]
            if t and t != ["object"]:
                return " or ".join(t)
    if "$ref" in node or "items" in node:
        return "array" if "items" in node else "object"
    return "any"


def _short(rid: str) -> str:
    return rid.split("/", 1)[1] if rid.startswith("rcodes:") else rid


def render_markdown(schema: dict[str, Any], report: dict[str, Any]) -> str:
    lines = [
        "# Application data schema (consolidated)",
        "",
        "Generated by `python -m rcodes.core.export_schema` from the base application schema and the",
        "Chapter 2, 3, 4 Part 1 and 4 Part 2 fact vocabularies. Do not edit by hand.",
        "The JSON Schema is `application.schema.json` in this folder.",
        "",
        schema["description"],
        "",
        f"{report['facts']} documented facts ({report['patterns']} name patterns with a `<type>` key),",
        f"{len(report['undocumented'])} facts read by rules but not documented in any FACTS.md.",
        "`null` means unknown and is allowed on every fact typed from FACTS.md (base-schema fields keep their base type). Used by: rule IDs as `<chapter>/<clause>`.",
        "",
    ]
    groups: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for name, node in _leaves(schema):
        groups.setdefault(name.split(".", 1)[0], []).append((name, node))
    for group, items in groups.items():
        lines += [f"## {group}", "", "| Fact | Type | Meaning | Used by |", "|---|---|---|---|"]
        for name, node in items:
            users = node.get("x-used-by", [])
            used = ", ".join(_short(u) for u in users[:6])
            if len(users) > 6:
                used += f" (+{len(users) - 6})"
            desc = node.get("description", "")
            if node.get("x-undocumented"):
                desc = "*undocumented* " + desc
            for n in node.get("x-notes", []):
                desc += f" Note: {n}"
            cell = lambda s: str(s).replace("|", "\\|")
            lines.append(f"| `{name}` | {cell(_type_label(node))} | {cell(desc)} | {cell(used)} |")
        lines.append("")
    if schema.get("x-usage-notes"):
        lines += ["## Usage notes not tied to one fact", ""]
        lines += [f"- {n}" for n in schema["x-usage-notes"]]
        lines.append("")
    return "\n".join(lines)


# --- validation and output ---------------------------------------------------------

def validate_cases(schema: dict[str, Any], registry: Registry) -> list[str]:
    from jsonschema import Draft202012Validator

    Draft202012Validator.check_schema(schema)
    v = Draft202012Validator(schema)
    errs: list[str] = []
    for pkg in registry.packages.values():
        for case in pkg.cases:
            for e in v.iter_errors(case.get("app", {})):
                where = "/".join(str(p) for p in e.absolute_path) or "<root>"
                errs.append(f"{case.get('_path')} [{case.get('title')}] {where}: {e.message}")
    return errs


def dump(obj: Any) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def export(out: Path, registry: Registry | None = None) -> dict[str, Any]:
    registry = registry or Registry.load()
    schema, report = build_schema(registry)
    out.mkdir(parents=True, exist_ok=True)
    (out / "application.schema.json").write_text(dump(schema), encoding="utf-8", newline="\n")
    (out / "application.md").write_text(render_markdown(schema, report), encoding="utf-8", newline="\n")
    report["case_errors"] = validate_cases(schema, registry)
    report["cases"] = sum(len(p.cases) for p in registry.packages.values())
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=Path("edition/schema"))
    args = ap.parse_args(argv)
    rep = export(args.out)
    print(f"facts {rep['facts']} (patterns {rep['patterns']}), undocumented {len(rep['undocumented'])}, "
          f"notes {rep['notes']} ({rep['loose_notes']} not tied to a fact)")
    print(f"cases {rep['cases']}, schema errors {len(rep['case_errors'])}")
    for e in rep["case_errors"][:40]:
        print("  " + e)
    return 1 if rep["case_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
