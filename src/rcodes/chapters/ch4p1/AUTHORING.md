# Chapter 4 Part 1 rule authoring guide

Read `../ch2/AUTHORING.md` (the base contract) and `../ch3/AUTHORING.md` (the twin method)
first. Everything in them applies here with the changes below.

Chapter 4 Part 1 covers apartments (multiple dwellings) in areas coded R10 to R60. Its
nearest twin is Chapter 3 (grouped dwellings): most of Parts 1, 3 and 4 are the same
provisions, while Part 2 (the building) has apartment-specific clauses on dwelling layout,
solar access, parking types and waste. Element numbering differs from Chapters 2 and 3:

| Chapter 4 Part 1 | Chapter 3 equivalent |
|---|---|
| 1.3 Communal open space | none (grouped has no communal open space element) |
| 1.4 Water management | 1.3 |
| 2.1 to 2.9 | 2.1 to 2.9 (no 2.10) |
| 3.8 Solar access for adjoining sites | 3.9 |
| 3.9 Visual privacy | 3.10 |
| 3.7 Access (14 clauses) | 3.7 (15 clauses; C3.7.15 is deleted here) |
| no retained dwellings element | 3.8 |

There is no pairing lint between this package and Chapter 3 (the clause numbers do not line
up), so byte-identity is not required. The method is still: start from the Chapter 3 file
for the same provision, check every value against the Chapter 4 Part 1 text, and change
what differs. Record in `notes` which Chapter 3 rule you started from (`from: ch3 C3.9.1`)
and, where the test changed, why (`diverges: ...`). Provisions with no Chapter 3 equivalent
are written fresh under the Chapter 2 guide.

## Sources

1. Draft text: `Working/text/draft/Residential Design Codes Chapter 4 (Part 1) - Apartments.txt`
   (page markers `===== PAGE n =====`; Chapter 4 Part 1 PDF page in `source.page`).
2. Register: `Working/register/ch4p1-apartments-r10-r60.csv` (`id` values `C4P1-001` to `C4P1-153`).
3. The Chapter 3 package `src/rcodes/chapters/ch3/` as the starting point.

## Coding and applicability

- `coding` is within `R10-R60` for every rule. Use the bands the text gives (`R10-R25`, `R30-R60` ...).
- `applies_to`: `["multiple_dwelling"]`, plus `"ancillary_dwelling"` where the clause says so.
- Per-dwelling provisions (floor areas, bedroom sizes, ceiling heights, storage, solar access
  to dwellings, private open space per apartment) are tested against facts that describe the
  least compliant dwelling (see FACTS.md usage notes), or against percentages of dwellings
  where the clause is written that way (70% of dwellings with two hours of sun).
- Parking is per Table 2.3a by Location A/B and bedroom count; the resident minimum, the
  2-bay average maximum (C2.3.4), visitor, motorcycle and bicycle provisions are separate rules.
  There is no regional table in this chapter: write one `conditional` rule with `region:
  regional` and `kind: judgment` noting the gap (register C4P1-048), not an invented value.

## Files you write

```
src/rcodes/chapters/ch4p1/
  rules/<element>/<clause>.json
  fallbacks/M<element>.json
  tables/table-<ref>.json          (copy from ch3 where the table is the same; same short id)
  tests/cases/<part>.json
  tests/cases/FACTS-PROPOSED-<part>.md   (only if needed)
```

Do not write meta.json, AUTHORING.md, FACTS.md or table-4A.json (except the 3.1 to 3.4
transcriber, who verifies table-4A.json against page 7). Do not touch another slice's
directories or anything under ch2/ or ch3/. No session, hand-off, messaging or scheduling
tools. Do not run pytest or install packages.
