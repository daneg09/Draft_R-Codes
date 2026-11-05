"""Published export layers: the JSON-LD graph (edition/graph) and the consolidated
application schema (edition/schema) are regenerated and must match what is committed."""

import json
from pathlib import Path

import pytest

from rcodes.core import export_jsonld, export_schema
from rcodes.core.registry import Registry

EDITION = Path(__file__).resolve().parents[1] / "edition"


@pytest.fixture(scope="module")
def reg() -> Registry:
    return Registry.load()


@pytest.fixture(scope="module")
def graph_out(tmp_path_factory, reg) -> tuple[Path, dict]:
    out = tmp_path_factory.mktemp("graph")
    return out, export_jsonld.export(out, reg)


@pytest.fixture(scope="module")
def schema_out(tmp_path_factory, reg) -> tuple[Path, dict]:
    out = tmp_path_factory.mktemp("schema")
    return out, export_schema.export(out, reg)


def _same_files(generated: Path, committed: Path) -> None:
    gen = sorted(p.name for p in generated.iterdir())
    com = sorted(p.name for p in committed.iterdir() if p.is_file())
    assert gen == com, f"file sets differ: generated {gen}, committed {com}"
    stale = [n for n in gen if (generated / n).read_bytes() != (committed / n).read_bytes()]
    assert not stale, f"stale in {committed}: {stale}; rerun the exporter"


def test_graph_matches_committed(graph_out):
    _same_files(graph_out[0], EDITION / "graph")


def test_schema_matches_committed(schema_out):
    _same_files(schema_out[0], EDITION / "schema")


def test_graph_edge_endpoints_exist(graph_out):
    out, rep = graph_out
    assert rep["dangling"] == []
    for p in sorted(out.glob("*.jsonld")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        assert "@context" in doc and doc["@graph"], p.name
        ids = [n["@id"] for n in doc["@graph"]]
        assert len(ids) == len(set(ids)), f"{p.name}: duplicate node ids"
        assert export_jsonld.dangling(doc) == [], p.name


def test_graph_covers_every_record(graph_out, reg):
    doc = json.loads((graph_out[0] / "edition.jsonld").read_text(encoding="utf-8"))
    ids = {n["@id"] for n in doc["@graph"]}
    for rec in reg.all_rules() + reg.all_fallbacks():
        assert export_jsonld.compact(rec.id) in ids, rec.id


def test_all_cases_validate_against_generated_schema(schema_out, reg):
    out, rep = schema_out
    schema = json.loads((out / "application.schema.json").read_text(encoding="utf-8"))
    assert rep["cases"] == sum(len(p.cases) for p in reg.packages.values()) >= 605
    assert export_schema.validate_cases(schema, reg) == []
