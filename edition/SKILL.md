---
name: rcodes-draft-assessment
description: Assess a residential proposal or plan against the draft WA Residential Design Codes (R-Codes) advertised 24 October 2026 (version draft-2026-10-24), using the machine-readable edition in this directory. Use when asked to check a single house, grouped dwelling or apartment proposal against the draft R-Codes, to answer what the draft requires for an element or clause (setbacks, parking, open space, privacy, overshadowing and so on), to say whether an LPP or LDP may vary a provision, or to list the facts a plan must supply before it can be assessed. Works with the Python engine (Mode 1) or from the edition files alone (Mode 2); both give the same report.
---

# Assessing a proposal against the draft R-Codes

## 1. What this is, and the honesty rules

This directory holds every provision of the draft consolidated R-Codes (Chapters 2, 3, 4 Part 1 and 4 Part 2, plus the Chapter 1 operation layer) as records with stable IDs, printed text, source pages and encoded tests. `README.md` describes the layers. Read it first, but do not read the directory whole.

- The draft is a consultation draft (consultation closes 26 February 2027), not law. Say so in every report. The published PDF governs wherever it differs from a record.
- Never guess a missing fact and never apply a default. Report **cannot tell**, name the fact, and ask for it.
- Cite every finding by chapter, clause ID and printed page, e.g. `ch2 C3.3.3`, p31. Use the full ID `rcodes:draft-2026-10-24/ch2/C3.3.3` once per report.
- A record marked ⚑ carries an ambiguity in the draft itself. Report it with the finding, quoting the note from the pack or `indexes/flagged.md`. Do not resolve it silently.
- Do not assess merit criteria (M), element objectives (O) or design guidance (DG). When a provision is not met, name the fallback record as the route to merit or performance assessment and stop there.
- Element numbers differ between chapters (3.3 is street setbacks in ch2 but tree canopy in ch4p2). Always give the chapter with the clause. Use `indexes/topics.md` to find a subject.

## 2. Mode 1: with Python

Run from the repository root (the directory above `edition/`) with `PYTHONPATH=src` set, or after `pip install -e .`.

1. **Build the application document** (`app.json`) from the plan. The fields are listed in `schema/application.md` (JSON Schema: `schema/application.schema.json`). Facts are dotted paths, so `parking.garage.setback_primary_m` is `{"parking": {"garage": {"setback_primary_m": 4.5}}}`. Start with `site.r_code`, `site.region` (`perth-peel` or `regional`), `site.area_m2` and `proposal.dwelling_type` (`single_house`, `grouped_dwelling`, `multiple_dwelling`). Then use `indexes/elements-to-facts.md` for what each element needs. Leave unknown facts out or set them to null: absent means unknown, never zero. Add a `facts_meta` entry for each numeric fact: `{"method": "stated|measured|computed|inferred|assumed", "confidence": 0-1, "source": {"file": ...}}`. A fact with confidence below 0.8 counts as missing. Put any LDP, LPP or scheme clause the applicant cites under `site.instruments`, as in `examples/r30-single-house.json` (`targets` gives chapter, clause and an `effect` such as `{"set": {"value": 4.5}}`, plus `reading_confirmed`).
2. **Applicability**: `python -m rcodes applicability app.json` returns the chapter (Table 1.1), the pathway and whether the R-Codes require a development application (Figure 2.1).
3. **Run**: `python -m rcodes run app.json --md` (or without `--md` for JSON).
4. **Read the report**:
   - Header: chapter, dwelling type, coding and **pathway**. `deemed-exempt` means every tested C provision is met. `merit-assessment` means at least one C provision is not met. `performance-assessment` is Chapter 4 Part 2. `undetermined` means some provisions are cannot tell.
   - Provision table: one row per provision with outcome (Meets, Does not meet, Cannot tell, Not applicable, Not evaluated), tested value, threshold, the exception or local variation used, missing facts and fallback. A Meets or Does not meet row that also lists `missing:` was tested, but one of its "Applies only when" facts is unknown. Report it as "meets/does not meet if it applies" and ask for that fact.
   - *Merit assessment required*: the elements with a provision not met, and the consultation that Table 2.4 recommends.
   - *Local instrument variations*: each cited clause, recognised or not, with the reason (permission level, WAPC approval, region, direction). "Reading not confirmed" means a planner has not checked how the clause was read. Say so.
   - *Missing facts*: grouped by the document that should supply them (site plan, landscape plan, lot plan, application form and so on).
   - Not evaluated: judgment provisions with no encoded test. List them as needing a planner's reading of the text, and do not decide them.
5. **Cannot tell**: ask for the named fact from the named source document, then re-run. Do not substitute a typical value. Recast the engine output into the report format in section 4.

## 3. Mode 2: without Python

Paths are relative to this directory.

1. Read `README.md`.
2. Pick the chapter from dwelling type and coding using Table 1.1 (in README, printed text in `chapters/ch1/operation.md`). R100-SL and R2-R5 multiple dwellings are not provided for. Figure 2.1 in the same file says whether a development application is needed.
3. Read the heading list of `chapters/<ch>/digest.md` (`## <element> <title>`). Choose the elements the plan engages: a single house usually touches about eight (open space, trees, parking, site cover, height, street and lot boundary setbacks, access, overshadowing, privacy).
4. For each element, open `elements/<ch>/<element>.md`. Find each provision by its heading (search ``^### `C3.3.3` ``) and read only that section. The digest line format is explained in README.
5. List the facts from each provision's `Facts:` line. Take them from the plan or ask the applicant ("Questions to ask the applicant" in the pack words the question).
6. Filter by the provision's coding, `applies to`, region and "Applies only when" conditions. A provision that fails a condition is not applicable. One whose condition fact is unknown is "if it applies".
7. Apply the test exactly as written: the threshold, or the table row for the coding or keyed fact. For rounding, follow the words beside `round(...)`. Try exceptions **in order**: an exception whose condition holds changes the test as stated. If the base test fails and an exception's condition is unknown, the outcome is cannot tell.
8. Decide **meets**, **does not meet**, **cannot tell** (name the fact) or **not applicable**. Judgment provisions are **not evaluated**: quote the text and leave the call to a planner.
9. If the applicant cites an LDP, LPP or scheme provision, read the pack's `Local variation` line, then `chapters/ch1/permissions.md` for the level (without WAPC approval, regional local governments only, WAPC approval) and the printed condition. Apply the variation only if the instrument may make it at that level, in that direction and region. Otherwise report it as not recognised, with the reason. The edition holds no local instrument text, so the applicant must supply the clause.
10. For anything not met, take the fallback from the provision's `Not met:` line (M, or O informed by DG in ch4p2). Check flagged notes (⚑) on every provision you used. Assemble the report.

## 4. Report format (both modes)

```
# Draft R-Codes assessment: <site>
Draft R-Codes draft-2026-10-24 (consultation draft, not in force; the PDF governs).
Site: <lot, LGA, region>. Coding: <R-code>. Dwelling type: <type>. Chapter: <ch>.
Pathway: <deemed-exempt | merit-assessment | performance-assessment | undetermined>. DA: <Figure 2.1 result>.

| Element | Clause ID | Outcome | Value tested | Threshold | Exception or variation used | Page |

## Elements on merit
- <element>: <clauses not met> -> fallback <M/O ID> (not assessed here)

## Missing facts
- <source document>: <fact>, <fact>

## Draft ambiguities encountered
- <clause ID>: <flag note, quoted or summarised>

## Summary
<One plain-language paragraph: what complies, what does not and what route it goes to, what is unknown and who must supply it.>
```

List only provisions that apply or might apply. Not-applicable rows may be counted in one line.

## 5. Worked excerpt (Mode 1)

`examples/r30-single-house.json`: a regional R30 single house (illustrative), garage 4.5 m from the primary street, and an LDP cl 3.2 setting a 4.5 m garage setback.

```
$ PYTHONPATH=src python -m rcodes run examples/r30-single-house.json --md
Chapter: ch2. Dwelling type: single_house. Coding: R30. Pathway: undetermined.
| 3.3 Street setbacks | C3.3.3 | Meets | 4.5 | >= 4.5 | ldp:LDP (illustrative) cl 3.2 (recognised); missing: parking.garage.present | M3.3 |
- ldp:LDP (illustrative) cl 3.2: recognised. applied; instrument reading not confirmed by a planner
- site plan: ..., parking.garage.present, ...
```

In the report:

```
| 3.3 Street setbacks | ch2 C3.3.3 | Meets, if it applies (parking.garage.present not stated) | 4.5 m | >= 4.5 m (Table 3.3c 5.0 m varied by LDP cl 3.2) | LDP: Table 2.5B allows all 3.3 clauses without WAPC approval; reading not confirmed | p31 |
```

The pathway stays undetermined while 94 provisions are cannot tell. Ask for the site plan and landscape plan facts.

## 6. Limits

- Plan reading is not part of the edition. Facts come from the applicant, or from your own reading of a plan. If you read a plan, record each fact with `method` (`measured` or `inferred`) and an honest `confidence` in `facts_meta`, and say in the report which facts you read yourself.
- There is no local-instrument data: no scheme, LPP, LDP or structure plan text. Only the Chapter 1 rules on what they may vary are included.
- There is no spatial data: no lot boundaries, R-coding maps, Location A or B, or Perth and Peel extents. Ask for coding, region and location.
- The R-Codes currently in force are not included. Do not compare against them from memory.
