"""Load and validate against the core JSON Schemas."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).parent / "schemas"


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _registry():
    from referencing import Registry, Resource

    resources = []
    for p in SCHEMA_DIR.glob("*.schema.json"):
        with p.open(encoding="utf-8") as fh:
            doc = json.load(fh)
        res = Resource.from_contents(doc)
        resources.append((doc["$id"], res))
        resources.append((p.name, res))
    return Registry().with_resources(resources)


@lru_cache(maxsize=None)
def validator(name: str) -> Draft202012Validator:
    schema = load_schema(name)
    try:
        return Draft202012Validator(schema, registry=_registry())
    except ImportError:  # referencing not installed; refs across files will not resolve
        return Draft202012Validator(schema)


def validate(name: str, doc: dict[str, Any]) -> list[str]:
    """Return a list of error messages (empty when valid)."""
    errs = sorted(validator(name).iter_errors(doc), key=lambda e: list(e.path))
    out = []
    for e in errs:
        where = "/".join(str(p) for p in e.path) or "<root>"
        out.append(f"{where}: {e.message}")
    return out


def assert_valid(name: str, doc: dict[str, Any], label: str = "") -> None:
    errs = validate(name, doc)
    if errs:
        raise jsonschema.ValidationError(f"{label or name} invalid:\n  " + "\n  ".join(errs))
