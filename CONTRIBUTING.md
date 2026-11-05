# Contributing

This repository transcribes a published document. A change is accepted when the page supports it. Read
[`edition/GOVERNANCE.md`](edition/GOVERNANCE.md) first.

## Reporting an error

Open an issue naming the clause ID (for example `rcodes:draft-2026-10-24/ch2/C3.3.3`) or table ID, the chapter and
the printed page, what the page says, and what the record says instead. If the page itself is ambiguous or
contradicts another page, say so: that is a flag on the record, not a correction.

## Correcting a record

1. **Edit the source record under `src/rcodes/chapters/<chapter>/`** (`rules/`, `fallbacks/`, `tables/`, or
   `data/` for Chapter 1 and Appendix A1). Never edit `edition/` by hand; it is regenerated.
2. **Cite the page.** Set `source.page` to the printed page, keep `text` verbatim from the page (including the
   draft's own errors), and update the `verified` stamp (`method`, `page`, `date`, `by`). If the page leaves the
   value uncertain, set `"verify": true` and say why in `notes`.
3. **Keep twins together.** Identical Chapter 2 and Chapter 3 rules are separate files held by the pairing lint;
   change both, or start the Chapter 3 record's `notes` with "diverges:" and say why.
4. **Log it in `CHANGELOG.md`** under a dated heading: the record, the field, the old and new value, the page and
   the reason. Wording corrections, flags cleared and draft inconsistencies confirmed are logged the same way.
5. **Run the tests**: `python -m pytest -q`. They must all pass.
6. **Regenerate the edition**, then run the tests again:

   ```bash
   python -m rcodes publish
   python -m rcodes export-jsonld
   python -m rcodes export-schema
   python -m pytest -q
   ```

   `tests/test_edition.py` and `tests/test_exports.py` fail until the committed `edition/` matches a fresh run.
   If a change alters a worked example outcome, update `edition/worked/` and `tests/test_worked.py` together and
   say why in the change log.

## Adding a test case

Test cases live in `src/rcodes/chapters/<chapter>/tests/cases/*.json`, each file a JSON list:

```json
{"title": "R60, upstairs living, 3 bed, balcony 12 m2 x 2.4 m: meets 2.1",
 "covers": ["rcodes:draft-2026-10-24/ch2/C2.1.1(ii)"],
 "app": {"site": {"r_code": "R60", "region": "perth-peel"}, "proposal": {"dwelling_type": "single_house"}},
 "expect": {"rules": {"rcodes:draft-2026-10-24/ch2/C2.1.1(ii)": "MEETS"}}}
```

`app` must validate against the application schema (`site.r_code` and `proposal.dwelling_type` are required) and
use facts from the chapter's `FACTS.md`. Each measurable or conditional rule needs at least one MEETS and one
DOES_NOT_MEET case, and a CANNOT_TELL case where an exception depends on a fact. Expected outcomes are `MEETS`,
`DOES_NOT_MEET`, `CANNOT_TELL`, `NOT_APPLICABLE` and `NOT_EVALUATED`. Base the values on the page, not on what the
engine currently returns.

## Authoring guides

Each chapter has a guide to its record shapes, fact names, evaluators and test cases. Read the whole guide
before writing a record in that chapter.

| Chapter | Guide | Fact vocabulary |
|---|---|---|
| Chapter 2 Single Houses | `src/rcodes/chapters/ch2/AUTHORING.md` | `src/rcodes/chapters/ch2/FACTS.md` |
| Chapter 3 Grouped Dwellings | `src/rcodes/chapters/ch3/AUTHORING.md` | `src/rcodes/chapters/ch3/FACTS.md` |
| Chapter 4 Part 1 Apartments R10 to R60 | `src/rcodes/chapters/ch4p1/AUTHORING.md` | `src/rcodes/chapters/ch4p1/FACTS.md` |
| Chapter 4 Part 2 Apartments R80 and above | `src/rcodes/chapters/ch4p2/AUTHORING.md` | `src/rcodes/chapters/ch4p2/FACTS.md` |

The guides name the transcription sources used to build the records (text extracts and a change register in a
`Working/` folder). That folder is not part of this repository; the published PDFs are the source for any
correction.

Engine changes (`src/rcodes/core/`) follow [`docs/DEVELOPING.md`](docs/DEVELOPING.md): no evaluator may call a
model or the network, and no rule may see a default for a missing fact.

## Scope

Changes that add the current code, local instruments, spatial data or plan reading are out of scope (see
`edition/GOVERNANCE.md`).
