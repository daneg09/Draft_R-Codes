# Draft WA Residential Design Codes: machine-readable edition

A machine-readable edition of the **draft consolidated Residential Design Codes (R-Codes)** of Western Australia,
version `draft-2026-10-24` (consultation draft advertised 24 October 2026; submissions close 26 February 2027),
with a Python reference engine that applies it to a proposal.

This is an unofficial transcription. The WAPC's published PDFs govern, the draft is not in force, and an
assessment made with this repository is not planning advice or a determination. See
[`edition/GOVERNANCE.md`](edition/GOVERNANCE.md).

**Not a developer?** Start with [HOW-TO-USE.md](HOW-TO-USE.md): a plain-English guide to downloading the
folder, opening it in an AI tool, asking your question and reading the result.

## The edition, and the evidence for its three claims

`edition/` holds every provision of the draft as a structured record with a stable ID
(`rcodes:draft-2026-10-24/ch2/C3.3.3`), the printed text, the source page and an encoded test, plus chapter
digests, element packs and indexes sized so a model can assess a plan without reading the whole repository.

**1. It can be done: every provision is a record.**
664 provisions across Chapters 2, 3, 4 Part 1 and 4 Part 2; 141 merit, objective and design-guidance records;
149 tables; the Chapter 1 operation layer (Table 1.1 applicability, Figure 2.1 development applications, Table
2.4 consultation, Tables 2.5A, 2.5B and 3.5A on what an LPP or LDP may vary, clause 2.5.2); Appendix A1
definitions (197 terms). A JSON-LD graph (`edition/graph/`) and one consolidated application schema of 409 facts
(`edition/schema/`) are exported from the same records.

**2. It is useful: a model can apply it to a plan.**
- Fresh-session tests: a new model session confined to `edition/` answered four of five test questions with
  clause and page citations at the first attempt; after the fixes logged in `CHANGELOG.md` it answered all five,
  plus a precinct structure plan case, reading about 10k tokens across twelve files.
- Worked example: [`edition/worked/two-storey-r20-15x30.md`](edition/worked/two-storey-r20-15x30.md) assesses a two-storey
  project home design, supplied by the owner as a single marketing page, on a 15 m x 30 m R20 lot, once from the plan alone and once with a
  declared siting. Its outcomes are pinned by `tests/test_worked.py`.

**3. It is verified as stated: one AI pass against the page image, no human review yet.**
Every value and text in the 805 rule and fallback records, and in the tables, was checked against the rendered
page image of the draft in one pass run by an AI model (Claude Opus 4.5, 2 November 2026; recorded in each
record's `verified` stamp as `"by": "opus-4.5-pass-1"`), with two value corrections. 123 records remain flagged
where the draft page itself is ambiguous, each with a note naming the problem (`edition/indexes/flagged.md`). No
human review of the records has been done yet; corrections are welcome by issue. Every
correction is logged with its page in [`CHANGELOG.md`](CHANGELOG.md). 605 authored test cases, the lint, the
Chapter 2 and 3 pairing check, and the regeneration of summary tables 2A, 3A, 4A and 2.1 from the rules all run
under `pytest`; the regeneration mismatches are draft inconsistencies, reported in `tests/`.

## Using it as a model reader

Point the model at `edition/` and let it follow the entry files; it should not read the directory whole.

| File | Use |
|---|---|
| [`edition/README.md`](edition/README.md) | what the edition contains, chapter selection (Table 1.1), reading method, statuses |
| [`edition/CLAUDE.md`](edition/CLAUDE.md) | short instructions for Claude Code |
| [`edition/SKILL.md`](edition/SKILL.md) | the assessment skill (`rcodes-draft-assessment`): run the engine, or apply the records by hand; one report format |
| [`edition/llms.txt`](edition/llms.txt) | every file in the edition, for tools that read `llms.txt` |

A single-house assessment typically reads the entry file, one chapter digest and about eight element packs.

## Running the engine and the tests

Python 3.11 or later.

```bash
pip install -e ".[dev,geometry]"
python -m rcodes applicability examples/r30-single-house.json --version draft-2026-10-24
python -m rcodes run examples/r30-single-house.json --version draft-2026-10-24 --md
python -m pytest -q
```

The tests run offline; no evaluator calls a model or the network. Commands, rule-file format, layout and the
engine's guarantees: [`docs/DEVELOPING.md`](docs/DEVELOPING.md). How to correct a record or add a test case:
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Repository layout

```
edition/          the published edition: generated recall layers, records, graph, schema,
                  plus the hand-written SKILL.md, GOVERNANCE.md and worked/
src/rcodes/core/      the engine (knows no chapter content), publish and export scripts, schemas, versions.json
src/rcodes/chapters/  the source records: one package per chapter (rules, fallbacks, tables, test cases,
                      authoring guide, fact vocabulary); ch1 holds the operation data and Appendix A1
examples/         application files (an illustrative R30 house, the two worked-example runs)
tests/            pytest suite and the regeneration and pairing reports
docs/             developer notes
```

The records under `src/` are the source. Everything in `edition/` except `SKILL.md`, `GOVERNANCE.md` and `worked/`
is generated (`python -m rcodes publish`, `export-jsonld`, `export-schema`), and the tests fail when the committed
copy is stale.

## Status and scope

Edition 1.0 of `draft-2026-10-24`, 3 November 2026. When the code is gazetted it will be added as a new version
with new clause IDs, linked to these by the `replaces` field on each record.

Out of scope: the R-Codes currently in force and an executable crosswalk to them; local instruments (schemes,
local planning policies, local development plans, structure plans) beyond the Chapter 1 rules on what they may
vary; spatial data (lot boundaries, coding maps, Location A or B, regional extents); reading plans. Facts are
supplied by a person or another tool and tested here.

## Licence, changes, governance

Licence: code under the MIT License and data and documents under Creative Commons Attribution 4.0 International (see `LICENSE` and `LICENSE-DATA`). The draft R-Codes text remains the copyright of the State of Western Australia; the published PDFs govern.

Changes: [`CHANGELOG.md`](CHANGELOG.md). Governance, citation and error reports:
[`edition/GOVERNANCE.md`](edition/GOVERNANCE.md). Citation metadata: [`CITATION.cff`](CITATION.cff).
