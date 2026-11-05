# Developing the engine and the records

Developer detail for the reference engine (`src/rcodes/`). The edition (`edition/`) is generated from the records
described here; see `../CONTRIBUTING.md` for how to correct a record and `../edition/GOVERNANCE.md` for the rules
that govern the edition.

## Setup and commands

```bash
pip install -e ".[dev,geometry]"
python -m rcodes summary
python -m rcodes lint
python -m rcodes applicability app.json --version draft-2026-10-24
python -m rcodes run app.json --version draft-2026-10-24 --md
python -m rcodes rules --version draft-2026-10-24 --chapter ch2
python -m rcodes publish            # regenerate edition/ (recall layers)
python -m rcodes export-jsonld      # regenerate edition/graph/
python -m rcodes export-schema      # regenerate edition/schema/
python -m pytest -q
```

Without installing, set `PYTHONPATH=src`. `compare app.json --versions V1 V2` runs several versions and pairs
results by `replaces`; only `draft-2026-10-24` has chapter packages in this repository, so it has nothing to pair
against yet.

`app.json` follows `src/rcodes/core/schemas/application.schema.json` (the consolidated, generated version with
every fact's meaning is `edition/schema/application.schema.json`). Every numeric fact should have a `facts_meta`
entry with `source`, `method` and `confidence`; a fact that is missing or below the confidence threshold (default
0.8) makes every rule that needs it return `CANNOT_TELL` with the fact named. Examples: `examples/`.

## Layout

```
src/rcodes/
  core/        engine; knows no chapter content (resolver, evaluators, report, lint, publish, exports)
  core/schemas/  rule, table, application, instrument and permission-table schemas
  core/versions.json  version declarations
  chapters/    one package per draft chapter: meta.json, rules/, fallbacks/, tables/, tests/cases/, data/,
               AUTHORING.md (authoring guide) and FACTS.md (fact vocabulary)
tests/         pytest suite; fixtures/pkg-ch2 is a two-rule stand-in for Chapter 2
```

A chapter package is data. The only code in a chapter package is an operation module (Chapter 1,
`chapters/ch1/operation.py`) that implements `applicability`, `da_required`, `consultation` and `permission`.

## Rule files

One JSON file per provision (`core/schemas/rule.schema.json`). Testable rules carry an `evaluator` of one of eight
types (threshold, table-lookup, percentage-of, formula, count, boolean, geometry, composite), ordered
`exceptions`, a `fallback` (the M, O or DG record), `replaces` edges to the code in force when the draft was
advertised, `source` page and printed `text`. `verified` records the page-image check (method, page, date, by).
`verify: true` means the record was checked but the page itself is ambiguous or inconsistent; the `notes` field
names the problem. Identical Chapter 2 and Chapter 3 rules are two files held together by the pairing lint
(`tests/test_pairing.py`).

## Guarantees

- No evaluator calls a model or the network. `pytest` runs offline.
- A rule never sees a default for a missing fact.
- A local instrument changes a rule only when the version's permission tables allow it; otherwise the base rule
  stands and the variation is reported as not recognised.
- The edition, graph and schema are deterministic; the tests require the committed copies to match a fresh run.

## Reports kept in `tests/`

`pairing-report.txt` and the `table-*-regeneration-report.txt` files are written by the test suite: the pairing
lint between Chapters 2 and 3, and the regeneration of summary tables 2A, 3A, 4A and 2.1 from the rules. The
mismatches they list are inconsistencies in the draft itself.
