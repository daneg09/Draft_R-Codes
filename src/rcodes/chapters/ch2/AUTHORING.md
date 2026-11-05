# Chapter 2 rule authoring guide

Read this whole file before writing a rule. It is the contract between the transcribers
of each part and the engine. The engine is in `src/rcodes/core/`; the two worked
examples are in `tests/fixtures/pkg-ch2/` (C3.1.1 and C3.3.3, with their fallbacks,
table and test cases). Copy their shape.

## Sources, in order of authority

1. The draft text extract: `Working/text/draft/Residential Design Codes Chapter 2 - Single Houses.txt`
   (page markers `===== PAGE n =====`; the PDF page number is what goes in `source.page`).
   The extract interleaves the two columns of each page, so read carefully and set
   `"verify": true` on any record where you are not certain of a number or a condition.
2. The change register: `Working/register/ch2-single-houses.csv`. Columns: id, draft_clause,
   draft_element, current_source, applies_to, current_provision, draft_provision, change_type,
   direction, ..., draft_page, current_page, notes. Use `draft_provision` for values,
   `current_source` and `change_type` for `replaces`, `notes` for `notes`, `id` for `register_ref`.
3. Do not open the current-code text. The crosswalk comes from `current_source`.

## Files you write (and only these)

```
src/rcodes/chapters/ch2/
  rules/<element>/<clause>.json        one per deemed exempt provision   e.g. rules/3.3/C3.3.3.json
  fallbacks/M<element>.json            one per element's merit criteria  e.g. fallbacks/M3.3.json
  tables/table-<ref>.json              one per table the rules look up    e.g. tables/table-3.3a.json
  tests/cases/<part>.json              a JSON list of test cases          e.g. tests/cases/part3a.json
```

Do not write meta.json, AUTHORING.md, FACTS.md or table-2A.json. Do not touch another
part's directories. Do not use any session, hand-off or messaging tool. Do not run the
tests (the integrator does). Do not install anything.

## IDs

```
rcodes:draft-2026-10-24/ch2/C3.3.3          a C provision
rcodes:draft-2026-10-24/ch2/C3.3.3-r1       an un-numbered sub-paragraph or reduction (suffix -r1, -r2)
rcodes:draft-2026-10-24/ch2/C3.3.2(ii)      a numbered sub-clause when it is a separate test
rcodes:draft-2026-10-24/ch2/M3.3            the merit criteria of element 3.3 (one record per element)
```

Table files are referenced by short name: `"table": "table-3.3a"`. The table file's `id`
field is the same short name.

Replaces IDs (current code), from the register's `current_source` column:

```
Vol1 Part B 5.2.1 C1.1      -> rcodes:vol1-v3-2026-04-10/partB/5.2.1-C1.1
Vol1 Part B Table B         -> rcodes:vol1-v3-2026-04-10/partB/T-B
Vol1 Part B Tables 2a/2b    -> rcodes:vol1-v3-2026-04-10/partB/T2a   (and T2b)
Vol1 Part C C3.3.4          -> rcodes:vol1-v3-2026-04-10/partC/C3.3.4
Vol1 Part C Table 3.3a      -> rcodes:vol1-v3-2026-04-10/partC/T3.3a
Vol1 Part D (definitions)   -> rcodes:vol1-v3-2026-04-10/partD/<term>
```

`relation` is the register's `change_type` (same, tightened, relaxed, restructured, renamed,
relocated, deleted, new, mixed, unclear). Use `"unchanged"` -> `"same"`. A new provision gets
`{"id": null, "relation": "new"}`.

## One rule per test

A clause that sets several independent tests becomes several rule files with suffixes or
sub-clause IDs. A clause whose tests are all-or-nothing becomes one rule with a
`composite` evaluator. A clause that merely cross-references other clauses ("must also
satisfy C3.1.1, C1.2.1 ...") is recorded once as `kind: conditional` with a `composite`
of `boolean` facts only if the applicant can answer them; otherwise make it `judgment`
with the cross-references in `notes`.

## Kind and column

- `kind: measurable` — a number or count against a threshold or table.
- `kind: conditional` — a yes/no condition the applicant can state as a fact
  (behind the street setback line, screened from the street, visually permeable).
- `kind: judgment` — needs a planner (contributes positively, adequate, compatible).
  No evaluator. Still a rule file so the element is complete.
- `column: C` for deemed exempt provisions. Merit criteria go in `fallbacks/` with
  `column: M`, `kind: judgment`, and the criteria text in `text`.
- Provisions that only apply to a coding band go in `coding`. "R40 and below" is
  `["R2-R40"]`; "R50 and above" is `["R50+"]`; R100-SL is the named code `"R100-SL"`.
  Where Table 2.10a modifies a value for R100-SL, write a separate rule file with
  coding `["R100-SL"]` and the main rule with coding excluding it (list the bands).
- `region`: `perth-peel`, `regional` or `all` (only parking differs).
- `applies_to`: `["single_house"]`; add `"ancillary_dwelling"` where the clause says so.

## Evaluators

Use the eight types in `core/evaluators.py`. Thresholds that depend on coding use
`table-lookup` or `{"table": "table-x"}` as the value of another evaluator. Keep rules
as data: no code.

- `threshold`: `{"type": "threshold", "fact": "...", "op": ">=", "value": 5.0}`
- `table-lookup`: `{"type": "table-lookup", "table": "table-3.3a", "fact": "...", "op": ">="}`;
  the table's `keys` are facts (usually `site.r_code`); a row `value: null` means no provision.
- `percentage-of`: `{"type": "percentage-of", "fact": "part", "of": "whole", "op": "<=", "value": 15}`
- `formula`: `{"type": "formula", "expr": "max(0.3 * site.frontage_m, 4)", "op": ">=", "value": {"fact": "..."}}`
- `count`, `boolean`, `composite` (`mode: all|any`, `parts: [...]`)
- `geometry` only where a polygon is the natural input (deep soil area, cone of vision); otherwise take the measured number as a fact.

Exceptions (concessions, reductions) go in `exceptions` in the order the clause lists
them, each with a `condition` evaluator and an `effect` (`set` a parameter, or
`replace_evaluator`, or `not_applicable: true`).

Applicability conditions that are not coding (climate zone, corner lot, frontage width,
storeys) go in `conditions` (a list of evaluators that must MEET for the rule to apply).

## Facts

Use only names in `FACTS.md`. If a provision needs a fact that is not there, add it to
`FACTS-PROPOSED-<part>.md` in your part's test directory with one line of justification,
and use it. Never invent a fact for something the applicant could not know.

## Every rule file carries

`source.page` (PDF page), `register_ref`, `verify` (true unless you checked the number
against the extract and it is unambiguous), `replaces`, `fallback` (`rcodes:draft-2026-10-24/ch2/M<element>`),
`notes` (register notes worth keeping, in your own words, short), `defined_terms`.

## Test cases

For each measurable or conditional rule, at least one case that MEETS and one that
DOES_NOT_MEET, and one CANNOT_TELL where an exception depends on a fact. Shape:

```json
{"title": "...", "covers": ["<rule id>"],
 "app": {"site": {...}, "proposal": {"dwelling_type": "single_house"}, ...},
 "expect": {"rules": {"<rule id>": "MEETS"}}}
```

`app` must validate against `core/schemas/application.schema.json` (site.r_code and
proposal.dwelling_type are required). Other rules in the package will also run on your
case; that is fine, only the rules you list are asserted.
