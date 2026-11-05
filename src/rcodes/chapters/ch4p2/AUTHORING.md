# Chapter 4 Part 2 rule authoring guide

Read `../ch2/AUTHORING.md` (the base contract) first. Chapter 4 Part 2 is different in kind
from Chapters 2, 3 and 4 Part 1: it is entirely performance-based. There are no deemed
exempt provisions and no merit criteria. Each element has **Objectives (O)**, **Acceptable
Outcomes (A)** that are one way of meeting them, and **Design Guidance (DG)**. The engine
treats an A like a C (a testable provision with a fallback) and O and DG like M (recorded,
never evaluated). Nothing here makes a proposal exempt from approval.

## Columns, kinds and IDs

| Record | `column` | `kind` | `fallback_kind` | ID |
|---|---|---|---|---|
| Acceptable Outcome | `A` | measurable, conditional or judgment | `O` | `rcodes:draft-2026-10-24/ch4p2/A2.2.1` |
| Objectives of an element | `O` | judgment | | `rcodes:draft-2026-10-24/ch4p2/O2.2` (one record per element, text holds O 2.2.1 to O 2.2.n) |
| Design Guidance of an element | `DG` | judgment | | `rcodes:draft-2026-10-24/ch4p2/DG2.2` (one record per element) |
| Table 2.1 row (a parameter the A cites) | `table` | | | tables only, see below |

`fallback` on every A record is the element's O record. O and DG records go in `fallbacks/`
(two files per element: `O2.2.json`, `DG2.2.json`). An A that is purely a judgment ("the
building responds to its context") is still a rule file, `kind: judgment`, no evaluator.
Sub-paragraphs of an A that are separate tests use `(i)` suffixes or `-r1` as in Chapter 2.

Text matters more here than in the other chapters because the Objectives are what an
applicant is assessed against. Put the printed objective and guidance text in `text` on the
O and DG records, cleaned of column interleaving, and set `verify: true` where the extract
is garbled.

## Table 2.1

Table 2.1 (pages 12 to 13) sets the default primary development parameters by coding column:
R80, LR1, R100, R160, MR1, MR2, HR1, HR2, HR3 and R-PA, for building height (storeys),
boundary wall height (storeys) and length, street setbacks, side and rear setbacks and plot
ratio. The columns are coding values, so rules look them up with `site.r_code` (the named
codes LR1, MR1, MR2, HR1, HR2, HR3, R-PA are known to the engine; R-AC4, R-AC3, R-AC1 and
R-AC0 are the current names and map to LR1, MR2, HR1 and R-PA).

`tables/table-2.1.json` is the summary form (keys `site.r_code` and `metric`) used by the
regeneration check; it is already written and the Part 2 transcriber verifies it against
page 13. Rules must not use it (a `metric` key is not a fact). Write operative per-metric
tables with the same short-id style the other chapters use:

```
table-2.1-height-storeys        keys site.r_code      value storeys (R-PA null: refer to scheme/LDP)
table-2.1-boundary-wall-storeys keys site.r_code
table-2.1-street-setback        keys site.r_code      value metres; the "2 m or nil" cells carry 2 with the nil as an exception on the rule conditioned on building.ground_floor_commercial (note 1)
table-2.1-side-setback          keys site.r_code      value metres; Nil = 0
table-2.1-rear-setback          keys site.r_code
table-2.1-plot-ratio            keys site.r_code      value ratio; N/A = null
table-2.2                       storeys to metres (relative building height)
table-2.7                       building separation by storey band, within site and to adjoining boundary
```

Table 2.1 is a default: Chapter 1B 3.5 and Table 3.5A let LPPs and LDPs amend or replace
it within conditions. The engine applies those variations through the instruments layer;
you only encode the defaults.

## Sources

1. Draft text: `Working/text/draft/Residential Design Codes Chapter 4 (Part 2) - Apartments.txt`
   (page markers `===== PAGE n =====`; PDF page in `source.page`).
2. Register: `Working/register/ch4p2-apartments-r80-plus.csv` (`C4P2-001` to `C4P2-132`).
   Its `current_source` column refers to Volume 2 (2024): write replaces IDs as
   `rcodes:vol2-2024/<clause>` such as `rcodes:vol2-2024/A2.2.1` or `rcodes:vol2-2024/T2.1`.
3. Chapter 4 Part 1 (`src/rcodes/chapters/ch4p1/`) for the apartment facts and for the Part 4
   elements that have a Part 1 twin (solar access, ventilation, size and layout, storage,
   dwelling mix, universal design, waste, utilities, parking). Start from those files where
   the provision is the same and note `from: ch4p1 <clause>`; this chapter's numbering wins.

## Facts

Use `FACTS.md` (the Chapter 4 Part 1 vocabulary plus an R80-and-above section). Propose
additions in `tests/cases/FACTS-PROPOSED-<part>.md`. Many Acceptable Outcomes here are
qualitative; make them `judgment` rather than inventing a yes/no fact for a quality.
Where an A gives a number (percent of dwellings, metres, storeys, a ratio, an area) it is
measurable.

## Coding

Every rule carries `coding` from this list, as the text applies it:
`["R80+", "LR1", "MR1", "MR2", "HR1", "HR2", "HR3", "R-PA", "LR", "MR", "HR"]`.
Provisions that depend on storey count or coding band (first four storeys, fifth storey and
above, "R80 to MR1") use `conditions` on `building.storeys` or coding bands.

## Files you write

```
src/rcodes/chapters/ch4p2/
  rules/<element>/<clause>.json
  fallbacks/O<element>.json, fallbacks/DG<element>.json
  tables/table-<ref>.json
  tests/cases/<part>.json
  tests/cases/FACTS-PROPOSED-<part>.md   (only if needed)
```

Do not write meta.json, AUTHORING.md, FACTS.md or table-2.1.json (except the Part 2
transcriber, who verifies table-2.1.json against page 13). Do not touch another slice's
directories or anything under ch2/, ch3/ or ch4p1/. No session, hand-off, messaging or
scheduling tools. Do not run pytest or install packages. Test cases: `pathway` for this
chapter is `performance-assessment` whatever the outcomes; assert rule statuses.
