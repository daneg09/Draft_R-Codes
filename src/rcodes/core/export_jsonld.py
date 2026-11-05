"""JSON-LD relationship graph of the draft edition: asserted relations only, no inference.

    python -m rcodes.core.export_jsonld --out edition/graph

Writes edition.jsonld (every node) and <chapter>.jsonld (a chapter's own nodes plus the
nodes they point at, so each file is self-contained). One node per line inside @graph.

Nodes: CodeVersion, Chapter, Element, Rule, Fallback, Table, DefinedTerm, Fact,
Instrument, CurrentClause. Edges, all read from record fields:

    inVersion    Chapter -> CodeVersion
    inChapter    Element, Rule, Fallback, Table -> Chapter
    inElement    Rule, Fallback -> Element
    fallbackTo   Rule -> Fallback                       (fallback)
    usesTable    Rule, Fallback -> Table                (evaluator / exception table refs)
    usesFact     Rule, Fallback -> Fact                 (inputs; evaluator, condition, exception facts)
                 Table -> Fact                          (table keys that are fact names)
    usesTerm     Rule, Fallback -> DefinedTerm          (defined_terms; Appendix A1 term, else undefined)
    replaces     Rule, Fallback -> CurrentClause        (replaces[].id, relation and note on the edge)
    variableBy   Rule -> Instrument (+ Table)           (rcodes.chapters.ch1.operation.permission)

Qualified edges (replaces, variableBy) are objects carrying the endpoint in "target" and the
relation's properties beside it.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from .export_schema import load_vocabularies, pattern_match, rule_facts
from .registry import PKG_ROOT, Registry
from .rules import ChapterPackage, Rule

VERSION = "draft-2026-10-24"
RC = f"rcodes:{VERSION}/"
INSTRUMENT_TYPES = ["ldp", "lpp", "scheme", "precinct_structure_plan"]
INSTRUMENT_TITLES = {"ldp": "Local development plan", "lpp": "Local planning policy",
                     "scheme": "Local planning scheme", "precinct_structure_plan": "Precinct structure plan"}
CH1_DATA = PKG_ROOT / "chapters" / "ch1" / "data"
PERMISSION_FILES = ["table-2.5A.json", "table-2.5B.json", "table-3.5A.json", "clause-2.5.2.json"]

CONTEXT: dict[str, Any] = {
    "@vocab": "https://riseurban.au/rcodes/vocab#",
    "rc": RC,
    "fact": "https://riseurban.au/rcodes/fact/",
    "term": "https://riseurban.au/rcodes/term/",
    "inst": "https://riseurban.au/rcodes/instrument/",
    "schema": "http://schema.org/",
    "title": "schema:name",
    "DefinedTerm": "schema:DefinedTerm",
    "inVersion": {"@type": "@id"},
    "inChapter": {"@type": "@id"},
    "inElement": {"@type": "@id"},
    "fallbackTo": {"@type": "@id"},
    "usesTable": {"@type": "@id", "@container": "@set"},
    "usesFact": {"@type": "@id", "@container": "@set"},
    "usesTerm": {"@type": "@id", "@container": "@set"},
    "replaces": {"@container": "@set"},
    "variableBy": {"@container": "@set"},
    "target": {"@type": "@id"},
    "table": {"@type": "@id"},
    "coding": {"@container": "@set"},
}

ID_EDGES = ["inVersion", "inChapter", "inElement", "fallbackTo", "usesTable", "usesFact", "usesTerm"]
QUALIFIED_EDGES = {"replaces": ["target"], "variableBy": ["target", "table"]}
TYPE_ORDER = ["CodeVersion", "Chapter", "Element", "Rule", "Fallback", "Table", "Instrument",
              "DefinedTerm", "Fact", "CurrentClause"]


def compact(full_id: str) -> str:
    return "rc:" + full_id[len(RC):] if full_id.startswith(RC) else full_id


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fact_id(name: str) -> str:
    return "fact:" + name.replace("<", "{").replace(">", "}")


# --- graph construction ------------------------------------------------------------

class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.home: dict[str, str | None] = {}  # node id -> chapter it belongs to (None = shared)

    def add(self, node: dict[str, Any], chapter: str | None) -> dict[str, Any]:
        nid = node["@id"]
        if nid in self.nodes:
            return self.nodes[nid]
        self.nodes[nid] = node
        self.home[nid] = chapter
        return node


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _terms_index() -> dict[str, dict[str, Any]]:
    doc = _load_json(CH1_DATA / "definitions-A1.json")
    index: dict[str, dict[str, Any]] = {}
    for t in doc["terms"]:
        for key in [t["term"]] + list(t.get("aliases") or []):
            index.setdefault(key.strip().lower(), t)
    return index


def _lookup_term(term: str, index: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    key = term.strip().lower()
    for cand in (key, key[:-1] if key.endswith("s") else None, key + "s"):
        if cand and cand in index:
            return index[cand]
    return None


def _table_refs(node: Any, out: set[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "table" and isinstance(v, str):
                out.add(v)
            else:
                _table_refs(v, out)
    elif isinstance(node, list):
        for x in node:
            _table_refs(x, out)


def rule_tables(rule: Rule) -> list[str]:
    out: set[str] = set()
    for key in ("evaluator", "conditions", "exceptions"):
        _table_refs(rule.data.get(key), out)
    return sorted(out)


def _variations(rule: Rule, op: Any) -> list[dict[str, Any]]:
    """Distinct permission results for every instrument type, direction and region."""
    seen: dict[tuple, dict[str, Any]] = {}
    for itype in INSTRUMENT_TYPES:
        for direction in ("increase", "decrease"):
            for region in ("perth-peel", "regional"):
                p = op.permission(itype, rule.chapter, rule.element, rule.clause, direction, region)
                if p.get("level") is None:
                    continue
                v = {"@type": "Variation", "target": f"inst:{itype}", "level": p["level"],
                     "table": compact(p["table"])}
                if p.get("direction"):
                    v["direction"] = p["direction"]
                if p.get("condition"):
                    v["condition"] = p["condition"]
                if p.get("verify"):
                    v["verify"] = True
                key = (itype, v["level"], v.get("direction"), v.get("condition"), v["table"])
                seen.setdefault(key, v)
    return [seen[k] for k in sorted(seen, key=lambda k: tuple(str(x) for x in k))]


def build(registry: Registry) -> tuple[Graph, dict[str, Any]]:
    g = Graph()
    vinfo = registry.version(VERSION)
    vid = f"rcodes:{VERSION}"
    g.add({"@id": vid, "@type": "CodeVersion", "title": vinfo["label"], "date": vinfo["date"],
           "status": vinfo["status"]}, None)
    op = registry.operation(VERSION)
    terms = _terms_index()
    vocab, _ = load_vocabularies()
    patterns = [n for n in vocab if "<" in n]
    stats = {"terms_linked": 0, "terms_undefined": 0, "tables_unresolved": []}

    for name in INSTRUMENT_TYPES:
        g.add({"@id": f"inst:{name}", "@type": "Instrument", "title": INSTRUMENT_TITLES[name], "code": name}, None)

    def fact_node(name: str) -> str:
        nid = fact_id(name)
        info = vocab.get(name)
        node = {"@id": nid, "@type": "Fact", "title": name}
        pattern = None if info else next((p for p in patterns if pattern_match(p, name)), None)
        if pattern:
            info = vocab[pattern]
            node["documentedAs"] = pattern
        if info:
            node["datatype"] = " | ".join(info["types"])
        else:
            node["documented"] = False
        g.add(node, None)
        return nid

    for name in vocab:
        fact_node(name)

    packages = sorted(registry.packages_for(VERSION), key=lambda p: vinfo["chapters"].index(p.chapter)
                      if p.chapter in vinfo["chapters"] else 99)
    table_home: dict[int, tuple[str, str]] = {}
    for pkg in packages:
        ch = pkg.chapter
        g.add({"@id": f"rc:{ch}", "@type": "Chapter", "title": pkg.meta.get("title", ch), "code": ch,
               "inVersion": vid}, ch)
        for el, title in (pkg.meta.get("elements") or {}).items():
            g.add({"@id": f"rc:{ch}/E{el}", "@type": "Element", "title": title, "number": el,
                   "inChapter": f"rc:{ch}"}, ch)
        for key, doc in sorted(pkg.tables.items()):
            if id(doc) in table_home:
                continue
            tid = f"rc:{ch}/{doc['id']}"
            table_home[id(doc)] = (tid, ch)
            node = {"@id": tid, "@type": "Table", "title": doc.get("title", doc["id"]), "inChapter": f"rc:{ch}"}
            page = (doc.get("source") or {}).get("page")
            if page is not None:
                node["page"] = page
            if doc.get("verify"):
                node["verify"] = True
            keys = [fact_node(k) for k in doc.get("keys") or [] if "." in k]
            if keys:
                node["usesFact"] = sorted(dict.fromkeys(keys))
            g.add(node, ch)

    # Chapter 1 permission tables
    ch1 = registry.package(VERSION, "ch1")
    if ch1 is not None:
        for fname in PERMISSION_FILES:
            doc = _load_json(CH1_DATA / fname)
            node = {"@id": compact(doc["id"]), "@type": "Table", "title": doc["title"], "inChapter": "rc:ch1",
                    "instruments": doc["instruments"], "chapters": doc["chapters"]}
            page = (doc.get("source") or {}).get("page")
            if page is not None:
                node["page"] = page
            g.add(node, "ch1")

    for pkg in packages:
        ch = pkg.chapter
        resolve = registry.table_resolver(VERSION, ch)
        records = [(r, "Rule") for r in pkg.rules.values()] + [(r, "Fallback") for r in pkg.fallbacks.values()]
        for rec, kind in sorted(records, key=lambda x: x[0].id):
            d = rec.data
            node: dict[str, Any] = {"@id": compact(rec.id), "@type": kind, "title": d.get("title", ""),
                                    "kind": d["kind"], "column": d["column"], "coding": list(d.get("coding") or [])}
            page = (d.get("source") or {}).get("page")
            if page is not None:
                node["page"] = page
            node["verify"] = bool(d.get("verify"))
            node["inChapter"] = f"rc:{ch}"
            eid = f"rc:{ch}/E{rec.element}"
            if eid not in g.nodes:
                g.add({"@id": eid, "@type": "Element", "title": d.get("element_title", rec.element),
                       "number": rec.element, "inChapter": f"rc:{ch}"}, ch)
            node["inElement"] = eid
            if kind == "Rule" and rec.fallback:
                node["fallbackTo"] = compact(rec.fallback)
            tables = []
            for ref in rule_tables(rec):
                doc = resolve(ref)
                if doc is None or id(doc) not in table_home:
                    stats["tables_unresolved"].append(f"{rec.id} -> {ref}")
                    continue
                tables.append(table_home[id(doc)][0])
            if tables:
                node["usesTable"] = sorted(dict.fromkeys(tables))
            facts = [fact_node(f) for f in rule_facts(rec)]
            if facts:
                node["usesFact"] = facts
            tnodes = []
            for term in d.get("defined_terms") or []:
                hit = _lookup_term(term, terms)
                if hit:
                    tid = "term:" + slug(hit["term"])
                    g.add({"@id": tid, "@type": "DefinedTerm", "title": hit["term"], "page": hit.get("page")}, None)
                    stats["terms_linked"] += 1
                else:
                    tid = "term:undefined/" + slug(term)
                    g.add({"@id": tid, "@type": "DefinedTerm", "title": term.strip(), "undefined": True}, None)
                    stats["terms_undefined"] += 1
                tnodes.append(tid)
            if tnodes:
                node["usesTerm"] = sorted(dict.fromkeys(tnodes))
            reps = []
            for r in d.get("replaces") or []:
                e: dict[str, Any] = {"@type": "Replacement", "relation": r.get("relation")}
                if r.get("id"):
                    cid = r["id"]
                    m = re.match(r"^rcodes:([^/]+)/", cid)
                    g.add({"@id": cid, "@type": "CurrentClause", "codeVersion": m[1] if m else None}, None)
                    e["target"] = cid
                if r.get("note"):
                    e["note"] = r["note"]
                reps.append(e)
            if reps:
                node["replaces"] = reps
            if kind == "Rule":
                var = _variations(rec, op)
                if var:
                    node["variableBy"] = var
            g.add(node, ch)
    return g, stats


# --- checks and output -------------------------------------------------------------

def edges(nodes: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    """(source, relation, target) for every edge, including both ends of qualified edges."""
    out = []
    for n in nodes:
        for rel in ID_EDGES:
            v = n.get(rel)
            for t in (v if isinstance(v, list) else [v] if v else []):
                out.append((n["@id"], rel, t))
        for rel, ends in QUALIFIED_EDGES.items():
            for e in n.get(rel) or []:
                for end in ends:
                    if e.get(end):
                        out.append((n["@id"], rel if end == "target" else f"{rel}.{end}", e[end]))
    return out


def dangling(doc: dict[str, Any]) -> list[tuple[str, str, str]]:
    nodes = doc["@graph"]
    ids = {n["@id"] for n in nodes}
    return [e for e in edges(nodes) if e[2] not in ids]


def counts(doc: dict[str, Any]) -> tuple[dict[str, int], dict[str, int]]:
    nodes = doc["@graph"]
    nt: dict[str, int] = {}
    for n in nodes:
        nt[n["@type"]] = nt.get(n["@type"], 0) + 1
    et: dict[str, int] = {}
    for _, rel, _ in edges(nodes):
        et[rel] = et.get(rel, 0) + 1
    return dict(sorted(nt.items(), key=lambda kv: TYPE_ORDER.index(kv[0]))), dict(sorted(et.items()))


def _sort_key(n: dict[str, Any]) -> tuple:
    return (TYPE_ORDER.index(n["@type"]), n["@id"])


def _closure(g: Graph, seeds: list[str]) -> list[dict[str, Any]]:
    keep: set[str] = set()
    todo = list(seeds)
    while todo:
        nid = todo.pop()
        if nid in keep or nid not in g.nodes:
            continue
        keep.add(nid)
        todo += [t for _, _, t in edges([g.nodes[nid]])]
    return sorted((g.nodes[i] for i in keep), key=_sort_key)


def serialise(nodes: list[dict[str, Any]], description: str) -> str:
    head = {"@context": CONTEXT, "description": description}
    lines = ["{"]
    for k, v in head.items():
        lines.append(f" {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},")
    lines.append(' "@graph": [')
    body = [" " + json.dumps(n, ensure_ascii=False, separators=(",", ":")) for n in nodes]
    lines.append(",\n".join(body))
    lines.append(" ]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def documents(registry: Registry | None = None) -> tuple[dict[str, str], dict[str, Any]]:
    """{filename: text} and build stats."""
    registry = registry or Registry.load()
    g, stats = build(registry)
    out = {"edition.jsonld": serialise(sorted(g.nodes.values(), key=_sort_key),
                                       f"Draft R-Codes {VERSION}: asserted relationships of every record. "
                                       "Generated by rcodes.core.export_jsonld; do not edit.")}
    chapters = sorted({c for c in g.home.values() if c})
    for ch in chapters:
        seeds = [i for i, c in g.home.items() if c == ch]
        out[f"{ch}.jsonld"] = serialise(_closure(g, seeds),
                                        f"Draft R-Codes {VERSION}, {ch}: the chapter's nodes and the nodes they "
                                        "reference. Generated by rcodes.core.export_jsonld; do not edit.")
    return out, stats


def export(out: Path, registry: Registry | None = None) -> dict[str, Any]:
    docs, stats = documents(registry)
    out.mkdir(parents=True, exist_ok=True)
    problems = []
    for name, text in docs.items():
        (out / name).write_text(text, encoding="utf-8", newline="\n")
        doc = json.loads(text)
        problems += [f"{name}: {s} -{r}-> {t}" for s, r, t in dangling(doc)]
    nt, et = counts(json.loads(docs["edition.jsonld"]))
    return {"files": sorted(docs), "nodes": nt, "edges": et, "dangling": problems, **stats}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=Path("edition/graph"))
    args = ap.parse_args(argv)
    rep = export(args.out)
    print("files:", ", ".join(rep["files"]))
    print("nodes:", ", ".join(f"{k} {v}" for k, v in rep["nodes"].items()), f"(total {sum(rep['nodes'].values())})")
    print("edges:", ", ".join(f"{k} {v}" for k, v in rep["edges"].items()), f"(total {sum(rep['edges'].values())})")
    print(f"terms linked {rep['terms_linked']}, undefined {rep['terms_undefined']}; "
          f"unresolved table refs {len(rep['tables_unresolved'])}")
    for t in rep["tables_unresolved"][:20]:
        print("  unresolved:", t)
    for p in rep["dangling"][:20]:
        print("  dangling:", p)
    return 1 if rep["dangling"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
