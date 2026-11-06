# Change log

Governance layer. Every correction to a record after its first transcription is listed here with the page that justified it. "Pass 1" is the page-image verification pass of 2 November 2026: one pass run by an AI model (Claude Opus 4.5), recorded in each record's stamp as `"by": "opus-4.5-pass-1"`. It is not human verification; no human review of the records has been done yet, and corrections are welcome by issue.

## 2026-11-02 Chapter 2 verification pass 1

Scope: all 151 rules, 24 merit records and 40 tables of Chapter 2 checked against rendered page images (130 dpi) of the draft PDF; printed text added to every record; `verified` stamp added. 26 records and 11 tables remain flagged `verify` because the page itself is ambiguous or internally inconsistent; each carries a note naming the ambiguity.

### Value corrections

| Record | Field | Old | New | Page | Reason |
|---|---|---|---|---|---|
| ch2/C1.1.1-r3 | coding | R17.5-R40 | R2-R40 | 9 | Table 1.1a: the "behind the street setback area" cell is merged across all rows including R2-R15; only the area, roof-cover and dimension cells read "no minimum applicable" |

### Verify flags cleared by the page

C2.2.2 (zones, 3 m x 3 m, 2 m shading and footnotes confirmed, p17); C3.2.1#height R100-SL 16 m (Table 2A cell spans R80 and R100-SL, p7); Table 3.4c R30-R40 65% is per boundary (Figure 3.4i, p35); Table 3.3a laneway rows for R2-R12.5 are "as per secondary street" in one merged cell (p29); Table 3.3b garage footnote excludes Table 3.3c garages from the reduced-portion width (p30); Table 3.5a bands take the nearest higher value (p36); Table 3.9a R80+ "no maximum" (p42); Table 3.9b keys confirmed (p43); Table 3.10a 3 / 4.5 / 6 m and the C3.10.1 trigger heading confirmed (p44); Table 2.10a R100-SL fences 900 mm (p25).

### Text corrections (wording only)

C2.1.1(ii) and M2.1: "private open space", not "private or public open space" (p15). M3.10: "of adjacent dwellings and adjoining properties" (p44). C3.3.2(i), C3.3.2(i)-r1: the draft's own "in accordance with in Table 3.3b" kept verbatim (p30). C3.7.2: "; or" before (iii) (p39).

### Draft inconsistencies confirmed on the page (left flagged)

- Table 3.4a wall-height bands leave 3.5 to 3.6 m and 7.0 to 7.1 m undefined; Table 2A labels the top band "7.1m and above" where Table 3.4a says "above 7.1m" (p7, p32).
- No rear setback is stated for R17.5 and above; Table 2A prints N/A (p7, p32).
- Table 2A boundary wall height 3.5 m printed from R2; Table 3.4c starts at R10 (p7, p34).
- Table 2A laneway (not primary street) N/A at R100-SL; Table 2.10a gives 0.5 m (p7, p25).
- Table 2.1a "2+ bedroom" and "3 or more bedrooms" rows overlap (p15).
- Table 2.3b column headed "Maximum ... R50 and above" prints 0/1/1/1 (p19).
- C2.6.2 "Notwithstanding C2.6.1(i)" cites the boundary cross-reference, not the wall height (p21).
- Table 2.10a cites C3.4.5 for boundary walls (should be C3.4.4) and C1.2.4 for trees (should be C1.2.3) (p25).
- C3.6.3 clause says "an upper floor balcony"; Figure 3.6a says "upper floor or balcony" (p37).
- Figure 3.4h labels R10-R25 walls "65% of lot boundary" against Table 3.4c's "greater of 9 m or 35%" (p35).
- C3.7.2 exceptions (i) and (ii) state no effect (p39).
- C4.1.7(ii) 50% cap on small dwellings is unworkable for a single lot; Table 2B R10-R25 averages are printed struck through with a Perth and Peel removal proposal (p50-51).
- Table 1.1b note 2 cites "Figure 1.1b"; the figure is labelled 1.1a (p10). Figure 1.1a legend counts eaves as covered; Table 1.1a note 1 excludes them (p9). Figures 4.1a-4.1c still cite "C1.1.3" and "Table D" (p50).

### Open structural items (encoding, not the page)

- C3.7.7 (and ch3 C3.7.7): the page triggers the 1 m truncation on access from any right-of-way; the condition uses `site.access_from_rear_row`. Change both twins together to `parking.access.street_type == row`.
- C3.6.4 (and ch3 twin): the "projected forward of the primary street setback line" trigger has no fact; the rule runs for any carport.
- C3.4.4#length-r50-wide: "cumulative maximum of 65%" is tested with the longest single wall; needs a cumulative fact.
- ch3 C1.1.1-r3: coding R17.5-R25 should become R2-R25 if the Chapter 3 Table 1.1a has the same merged location cell (to confirm in the Chapter 3 pass).
- `defined_terms` on rules cite 45 terms with no Appendix A1 entry (ordinary words or near-matches such as "soft landscaping" for "soft landscape"); clean up when the recall layers are generated.

## 2026-11-02 Definitions layer

Appendix A1: 197 terms transcribed verbatim from pages 4 to 11 of the Appendices, page-verified. Two flagged for the draft's own wording: "significant existing tree" (and/or structure) and "street setback line" (cites Part B Table B and Part C Table 3.3a, which no longer exist).

## 2026-11-02 Chapter 3 verification pass 1

Scope: all 180 rules, 24 merit records and 40 tables of Chapter 3 checked against rendered page images; printed text added; `verified` stamp added. Pairing with Chapter 2 preserved.

### Value corrections

| Record | Field | Old | New | Page | Reason |
|---|---|---|---|---|---|
| ch3/C1.1.1-r3 | coding | R17.5-R25 | R2-R25 | 9 | Table 1.1a "behind the street setback area" cell merged across all rows, as in Chapter 2 |

### Wording corrections

C2.1.1(ii), M2.1 (private open space), M2.7 (deemed-exempt column note removed from merit text), C2.10.1(i) ("; and"), C3.7.7 ("excludes a right-of-way as a street"), M3.10, C3.10.5-r1, C3.3.2(i) (draft's "in accordance with in"), C3.3.4, C3.4.5 ("provisions"), titles of C4.1.1-r1 to -r6 and M4.1.2 (Table 3B not 2B).

### Settled on the page

Table 2.3a visitor ratios 0.1 (Location A) and 0.15 (Location B) with the five-dwelling trigger (p19); C2.7.1 ten-dwelling trigger (p23); storage heading has no density qualifier (p15); C3.1.1 site basis is each dwelling's own site per A1 "site" (ii) with no share of common property (p28, p51); C3.4.1(ii) R2-R25 (p33); Table 3A R100-SL 16 m and 4 storeys cells span R80 and R100-SL (p7); C3.4.6 wording and Figure 3.4l (p35).

### Draft inconsistencies confirmed (left flagged)

As for Chapter 2, plus: C2.2.2 footnote 1 attached to grouped dwellings gives relief only to single houses (p17); C3.3.2(iii) still says "where a single house results from a subdivision" (p31); Figure 3.3d shows superseded 2.5 m / 1.5 m communal street setbacks while Table 3.3a has no communal street row (p30, p32); C3.7.14 cites C1.3.3, which does not exist (p42); Table 2.10a cites C1.1.1 for the primary garden area where C1.1.3 is meant and Figure 1.2c cites C1.1.1 and C1.1.2 for C1.1.3 and C1.1.4 (p26, p12); Figure 3.4i groups W3, W4 and W5 under one 65% limit on boundary C, so the R30-R40 length limit is cumulative per boundary (p36).

### Open structural items (added)

- Correction to the Chapter 2 entry: the twin of ch2 C3.7.7 (right-of-way truncation) is ch3 C3.7.9, not ch3 C3.7.7.
- Boundary wall length at R30-R40 and R50 is cumulative per boundary (Figure 3.4i); `building.boundary_walls.max_pct_of_boundary` measures the longest single wall. Both chapters need a cumulative fact.
- C3.7.5 and C3.7.6 share one fact for two different requirements (passing points every 30 m; 5.5 m x 6.3 m arterial entry).
- ch2 C3.7.10 text reads as garbled; recheck against the Chapter 2 page.
- Exception `source` strings copied from Chapter 2 cite Chapter 2 pages in ch3 records (C2.6.1-r1, C3.9.1); left because exceptions are part of the pairing signature.

## 2026-11-02 Chapter 4 Part 1 verification pass 1

Scope: all 164 rules, 23 merit records and 39 tables checked against rendered page images; printed text added; `verified` stamp added.

### Value corrections

None. Every encoded threshold, row, band and condition matched the page.

### Wording corrections

M2.7 (deemed-exempt column note removed from merit text, p23); M3.3 (corrupted "façade" character, p29); C3.4.5 ("provisions", p34); C3.3.1#communal-street (unprinted explanation moved to the verified note, p29); C3.7.7 ("excludes a right-of-way as a street"; exception source page, p40); M3.9 (p44); C3.9.5-r1 (C3.9.6(iii) as printed, p45); M4.1.2 and M4.1.4 (clause numbers restored, p49-50).

### Settled on the page

Table 2.3a: resident parking "No minimum" in one cell spanning Locations A and B with no bedroom split; visitor 0.1 (A) and 0.15 (B) per dwelling with no five-dwelling trigger; bicycle 0.5 resident and 0.1 visitor; motorcycle 0.1 for developments exceeding 20 dwellings (p19-20). C2.3.4 two-bay average at R50 and above with no Perth and Peel qualifier (p19). Table 2.1a 37/47/67/72/90/95 m2 with the toilet and bathroom note carrying no footnote marker (p16). C2.1.7 "more than 10 apartments"; C2.7.1 "10 or more" (p16, p23). C2.8.1 dual key 70 m2; C2.9.1 60 m2 (p24-25). Table 1.1a applies to all apartments with no coding split (p9); C1.2.6 not limited by dwelling type (p11); no 1.5 m street-setback trigger for trees in this chapter (p10). Table 4B prints the R10-R25 averages without strikethrough, unlike Chapter 3 Table 3B (p51). No single-storey overshadowing exemption and no R80+ row in Table 3.8a (p42-43). C3.7.2 has no R40 qualifier; C3.7.11 has no dwelling threshold (p39, p41). Table 3.4a gives one set of side setbacks for R10-R60 by wall height; only C3.4.1(ii) distinguishes R10-R25 (p32-33).

### Draft inconsistencies confirmed (left flagged)

- Table 4A side setback above 7.1 m prints 3.5 m; Table 3.4a prints 2.0 m; Figure 3.4l shows 3 m each side (p7, p32, p35). 2.0 m stays encoded.
- Table 4A rear setback at R10-R15 prints 6 m; Table 3.4a prints 3 m (p7, p32). 3 m stays encoded.
- No rear setback from R17.5; Table 4A prints N/A (p7, p32).
- Wall-height band gaps 3.5-3.6 m and 7.0-7.1 m (p32).
- Figure 3.4l building separation 6 m matches neither twice 2.0 m nor twice 3.5 m (p35).
- Table 3.2a prints "R2-R35" and Table 3.3c "In areas coded R2 - R35" in an R10-R60 chapter (p28, p31).
- Cross-references use Chapter 3 numbering: "3.9 Solar access", "3.10 Visual privacy", "C3.10.4", "Table 3.10a", "Table 3.9a" (p28, p32, p35, p42, p44-45).
- C2.1.2 cites Table 2.1a (dwelling sizes) for private open space; C2.3.7 cites a Table 2.3b that does not exist; footnote 2 cites "Table 2.3"; C2.6.1(iii) cites C1.1.1 for the primary garden area; C2.9 heading cites C4.1.3 while the clause cites C4.1.4 (p15, p19-20, p22, p25).
- C4.1.2 heading says "minimum site area" for an average clause; C4.1.3 to C4.1.6 and M4.1.4 refer to a "minimum" site area where Table 4B prints averages only; C4.1.7 cross-refers to C4.1.3 for the concessions (p49-51).
- Table 1.1a is titled "Primary garden area provisions" for apartments; Table 2.8a mixes "apartments" and "dwellings"; Table 1.3a note reads "co-indoor communal spaces" (p9, p12, p24).
- Figure 2.2a prints "Min dimension = 0.5 x wall height" with no matching limb; Figure 2.2b legend refers to single houses and grouped dwellings (p18).
- Figure 3.3c captioned "Figure 3.3s"; Figure 3.3d cites Part B clause 5.1.2 and "Table B column 7"; Figure 3.4h labels 65% against Table 3.4c's 35%; Table 3.4c note cites C3.4.5 for wall height (p31, p34-35).
- Merit criteria on p40 carry a "P" prefix.

### Open structural items (added)

- C3.6.1-r1 trigger `site.adjoins_public_open_space` is carried from Chapter 3; this page says only "where applicable".
- C3.7.9 right-of-way truncation and C3.7.5 / C3.7.6 shared fact: same as Chapter 3.
- C3.4.4#length-r50-wide cumulative test: same as Chapters 2 and 3.
- The transcriber's regional-parking gap record (C2.3.1-r1) stands: the draft has no regional parking table for apartments.

## 2026-11-02 Chapter 4 Part 2 verification pass 1

Scope: all 169 Acceptable Outcome records, 35 Objective and 35 Design Guidance records and 27 tables checked against rendered page images; Objective and Design Guidance text corrected where column reassembly had gone wrong; `verified` stamp added.

### Value corrections

None in rules. Table 3.4 gained the missing "up to 10 dwellings" hard landscape row (value N/A, one merged cell on p34).

### Text corrections

Design guidance reassembly: DG3.8 (items of DG 3.8.1 and 3.8.4 reassigned, p44), DG4.7 (items reassigned across DG 4.7.1 to 4.7.3, p66), DG4.4 (wintergardens bullet moved to DG 4.4.5; footnote restored, p59), DG4.14 (CPTED item completed, p79), DG4.11 and DG4.12 (unprinted lead-in and parenthesis removed, p73, p75), DG2.2 (capitalised list items, p15), DG3.7 (truncated "from vehicle" kept as printed, p42), DG3.9 (p47-48), DG4.1 to DG4.6 ("(new)" tags removed; they came from the register, not the page). A2.2.1-r1 text added (p15). Dashes and the cedilla in facade restored where the page prints them. Table 3.4 row text on A3.4.1-r3 (p34).

### Settled on the page

Every Table 2.1 cell in all ten code columns (p13). Note 1 (nil street setback with ground-floor commercial use) marks LR1, MR1-MR2 and HR1-HR3 only; note 4 (boundary walls both sides, two-thirds length) marks R80, R100 and R160 only; note 2 is on the boundary-wall row header for every code (p13). Table 2.2 is indicative (DG 2.2.1, p14-15). Table 2.7: within-site 3 m up to 4 storeys and 6 m at 5 and above; to an adjoining boundary at 5 storeys and above 9 m (land coded R60 or below) and 6 m (R80 or above), MR2 and HR codes only (p22). Table 3.3a deep soil 10% or 7% applies to every site size (merged cell, p31). Table 3.3b widths (p31). Table 3.4 communal open space (p34). Table 3.5 setbacks 3 / 4.5 / 6 m for the first four storeys; fifth storey and above refers to Table 2.7 in one merged cell (p36). Table 3.9: resident "No minimum"; visitor none for 0-4 dwellings then 0.1 (A) or 0.15 (B); bicycle 0.5 resident and 0.1 visitor; motorcycle 0.1 above 20 dwellings; rounding footnote on car and bicycle rows only (p46). A3.9.3 two-bay average (p46). Table 4.3a 36/47/67/90 m2 with the toilet and bathroom footnote marked on the 2 and 3 bedroom rows only; bedroom 10 and 9 m2 at 3 m excluding robes (the extract printed the superscript marker as "13m") (p55). Table 4.3b living rooms 3.6 m and 4 m (p56). Table 4.4 8/10/12/15 m2 at 2.0/2.4/2.4/3 m (p58). Table 4.6 in m2 (3/3/4/5), 1.5 m and 2.1 m, printed as "Table 4.6a" (p62). A4.2.2 60% in the first nine storeys (p52). A4.9.1 silver 20% or platinum 5% (p69). Table 4.12 soil depths printed as ranges for shrubs and ground cover; lower bounds encoded (p74). A4.15.1 0.5 NatHERS stars (p80). A4.10.5 awnings where the street setback is 1 m or less (p71).

### Draft inconsistencies confirmed (left flagged)

- A2.2.1-r1 and the derived metres table: Table 2.2 is indicative; the outcome is in storeys.
- A2.4.1: nothing says whether a boundary wall is an exception to the 4 m side setback; note 4 does not say two-thirds of what; note 3 gives no order among named codes (p13, p18).
- A2.7.1 and Table 2.7 adjoining rows: whose storeys are measured; uncoded or R100-SL adjoining land is not placed (p22).
- Element 3.1 prints no Objectives (p26). A3.2.3-r1 "reduced proportionally" gives no method (p28). A3.3.1 criteria mix AND with AND/OR (p31). A3.3.5-r3 wording for sites over 1,000 m2 (p31). A3.4.3 two continuous hours (p34). A3.8.1 part-20 m frontage (p43). A3.8.6 trigger list conjunction (p43). A3.8.7 driveway and corner cases run together (p43). A3.9.1 versus DG 3.9.8 on visitor bicycle parking (p46-47). Rounding footnote missing from the motorcycle row (p46). A3.9.3 visitor bays and the maximum (p46). A3.9.10 "above ground" undefined (p46).
- A4.2.1 "habitable rooms have openings on at least two walls" reads per room (p52). A4.3.1 footnote marker placement (p55). A4.8.1 limbs (a) and (b) overlap (p68). DG 4.18.4 prints "900m" (p87).
- Cross-reference and typographic faults: every Acceptable Outcomes box cites "(clause 1.2)" (p15-22); note 5 says "within this SPP" (p13); Table 2.7 first row says "All R-Codes" (p22); Figure 3.5b cites "Table 3.10a" (p37); 4.2 figures numbered 4.1a-4.1c (p52-53); A4.6.1 cites "Table 4.6" for "Table 4.6a" (p62); 4.18 cites "3.7 Public domain interface" for 3.6 (p86); DG 4.13.4 cites the repealed Heritage of Western Australia Act 1990 (p77); A4.1.4 and O4.1.3 omit climate zone 2 (p50); two Table of Changes claims for 4.12 and 4.14 have no text on the pages (p75, p79).

## 2026-11-02 Chapter 1 verification pass 1

Scope: Table 1.1, Figure 2.1, Table 2.4, Tables 2.5A, 2.5B, 3.5A and clause 2.5.2 checked against page images. No permission level differed from the page. Printed page numbers run seven behind the PDF page; `source.page` holds the printed page and `pdf_page` the PDF page.

### Corrections

- clause 2.5.2: `chapters` reduced from ch2, ch3, ch4p1, ch4p2 to ch2, ch3, ch4p1. Clause 2.5.2 sits in Chapter 1A; Chapter 1B (3.5.1, 3.5.2) gives precinct structure plans only the right to augment Chapter 4 Part 2 with Objectives, with WAPC approval, and does not mention schemes (p11, p15). Test expectation in tests/test_ch1.py updated to match.
- Tables 2.5A and 2.5B: element 2.10 restricted to ch2 and ch3; condition texts replaced with the printed wording for C2.3.1, C2.3.3, C2.3.5, 2.8, C3.3.1, C3.4.4, solar access and visual privacy rows (p12-13).
- Table 3.5A: printed condition wording for A2.2.1, A2.3.1, A2.4.1, A2.7.1, 3.5, A3.9.2; element titles as printed (p16).
- Table 1.1 and Figure 2.1: printed titles and text added to every row; Table 1.1 footnote on mixed use added (p4, p6).

### Left flagged

Table 2.4 streetscape clause references (C3.6.7, C3.6.8, 3.6.9 do not exist, p9). Table 2.5A: merged colour cells split into separate rows (water 1.3/1.4; C2.1.1 and C2.1.8/C2.1.9; C2.3.3/C2.3.5; solar 3.9/3.8; visual privacy C3.10.1/3.9.1); 2.6 printed twice; 2.8 cell uncoloured with a condition; "C4.4.4" for C3.4.4 (p12). Table 2.5B: merged cells; 3.4 and 3.10/3.9 clause cells blank (p13). Table 3.5A: A2.4.1 mixes directions; "A2.6.1" printed for building separation (p16). Clause 2.5.2: one row covers both schemes and precinct structure plans, so a precinct structure plan variation of a merit criterion is over-reported as untabled.

## 2026-11-02 Recall layers, graph and schema (step 3)

- `python -m rcodes publish` generates `edition/`: README.md, CLAUDE.md, llms.txt; one digest per chapter (5.1k to 6.5k tokens); 106 element packs (median 1.8k tokens, ten over 5k, largest ch3 element 3.4 at 10.6k); indexes (facts to rules, elements to facts, rules.json, flagged.md); A1 definitions; the JSON records copied verbatim. `tests/test_edition.py` fails when the committed edition is stale and warns on packs over budget.
- `python -m rcodes export-jsonld` writes `edition/graph/`: 2,097 nodes and 11,731 asserted edges (inChapter, inElement, fallbackTo, usesTable, usesFact, usesTerm, replaces, variableBy). 45 cited defined terms have no Appendix A1 entry and are flagged undefined; 466 current-code clause nodes come from `replaces` fields.
- `python -m rcodes export-schema` writes `edition/schema/`: one consolidated application schema generated from the four FACTS.md files (409 facts, each with meaning and the rules that read it); all 605 authored cases validate. Facts typed from FACTS.md accept null for unknown.
- `tests/test_exports.py` regenerates both and fails when stale.

## 2026-11-02 Encoding fixes after fresh-session test

### Visitor parking rate keyed on location (ch3, ch4p1, ch4p2)

- ch3 C2.3.3, ch4p1 C2.3.5 and ch4p2 A3.9.2-r1 computed the rate as `0.1 if site.location == 'A' else 0.15`, so any location value other than "A" was treated as Location B. The threshold now comes from a new table keyed on site.location with rows A and B only: `table-2.3a-visitor-bays` (ch3, ch4p1) and `table-3.9-visitor-bays` (ch4p2). Each row value is the bay-count expression (0.1 or 0.15 x proposal.dwelling_count, rounded as before), and the formula evaluator reads it through `{"table": ...}`. A missing site.location gives CANNOT_TELL with site.location named as missing. Values, rounding and the five-dwelling conditions are unchanged.
- A location value other than A or B matches no row. `ev_formula` in core/evaluators.py does not yet turn a null threshold into NOT_APPLICABLE, so intake must reject such values against FACTS.md (A / B). That needs a core change.
- Other `if ... else` formulas checked and left alone: ch4p1 C2.1.6 and ch4p2 A4.3.1 (bedroom-count ladder; "else 90" is the printed 3+ bedroom row), ch4p1 C2.8.1 (numeric dwelling-count split), ch4p2 A3.3.7 (boolean significant_tree_retained) and ch4p2 A3.8.6 (street class is one of three named classes). All of them give CANNOT_TELL when a fact is missing, and none falls back to a default for an unrecognised value.
- Reference table notes updated: ch4p1 table-2.3a-visitor, ch4p2 table-3.9-visitor.

### Garage setback applies only where a garage is proposed (ch2, ch3, ch4p1)

- C3.3.3 (ch2 and ch3 R2-R35, ch4p1 R10-R35) gains the condition `parking.garage.present == true` and the input parking.garage.present, matching C3.3.3#r40-plus. The ch2/ch3 pair stays identical. Authored cases that test C3.3.3 already state parking.garage.present true.

### Side setback bands conditioned on walls in the band (ch2, ch3, ch4p1)

- The upper band rules carried a condition on building.max_wall_height_m (> 3.5 m for 3.6-to-7m, > 7.0 m for over-7.1m), and the to-3.5m band had none. Under those conditions any building with a wall over 7 m was tested against both upper bands, and every building was tested against the lowest band, whether or not it had walls there. Each band rule now has a boolean presence condition, and the max-height condition and input are gone:
  - C3.4.1#side-to-3.5m, -r50 (ch2, ch3), -r30-r40 (ch3), -r30-r60 (ch4p1): building.has_walls_to_3_5m
  - C3.4.1#side-3.6-to-7m and the same variants: building.has_walls_3_6_to_7m
  - C3.4.1#side-over-7.1m and the same variants: building.has_walls_over_7_1m
- Band thresholds, the pedestrian access way exceptions and the rounding-gap notes are unchanged. The ch2/ch3 twins received the same edit. The three facts are added to each chapter's FACTS.md.
- 123 authored cases (ch2 37, ch3 40, ch4p1 46) now state the presence facts: true where the case supplies the band's setback, false where the stated maximum wall height rules out the band. building.max_wall_height_m stays in place because C3.9.1 still reads it. The table regeneration probes in tests/chapter_checks.py now use the presence facts.

### New cases

- Location not stated, CANNOT_TELL: ch3 C2.3.3, ch4p1 C2.3.5, ch4p2 A3.9.2-r1.
- Per chapter (ch2, ch3, ch4p1): a building whose walls are all 7.5 m high meets C3.4.1#side-over-7.1m with the lower bands switched off; a building with walls 3.6 to 7 m high but no setback stated for them gives CANNOT_TELL for C3.4.1#side-3.6-to-7m and MEETS for #side-to-3.5m.

## 2026-11-02 Edition revision after the first fresh-session test

A fresh Opus session confined to `edition/` answered four of five test questions correctly with clause and page citations on about 18k tokens of content. The fifth (what an LDP or LPP may vary) failed because the edition had no Chapter 1 operation layer. Changes:

- `edition/chapters/ch1/operation.md` (Table 1.1, Figure 2.1, Table 2.4, clause 2.5.2 scope) and `permissions.md` (what an LPP and an LDP may vary per chapter and element, with level and printed condition, from Tables 2.5A, 2.5B and 3.5A); every element pack carries a "Local variation" line pointing to it.
- README states what the edition contains and omits, gives measured sizes, and describes the intended reading method (digest heading list, then search by clause ID inside the pack).
- Digests use full words, titles cut at word boundaries, same-titled rules disambiguated by region or scope; packs carry a `Facts:` line under every heading.
- Core: a formula whose table-sourced threshold has no row returns NOT_APPLICABLE (`evaluators.ev_formula`), with a test.

## 2026-11-02 Second fresh-session test

Same five questions plus a precinct structure plan case under Chapter 4 Part 2. A fresh Opus session confined to `edition/` answered all five correctly with clause and page citations, reading about 40 KB (about 10k tokens) across twelve files by following the README method. Residual findings to fold into the skill pass: explain the digest line format and its field codes in the README; align CLAUDE.md and README on where local-variation questions go; say that element numbers differ between chapters; the ch4p1 2.3 "Local variation" line lists C2.3.1 twice without its two conditions; add a topic index (title keyword to rule IDs across chapters); express the rounding rule in words beside `round(x + 0.001)`.

## 2026-11-03 Worked example renamed

The worked example was renamed to `two-storey-r20-15x30` (examples, worked page, reports, tests, README and llms.txt links) and its brochure references were removed; the facts, values and engine outcomes are unchanged.

## 2026-11-03 Engine fixes from the worked example

Found by running the worked-example plan (`edition/worked/two-storey-r20-15x30.md`) through the engine. Core only; no rule, table or FACTS file changed.

- Unknown region (`core/resolver.resolve`): when `site.region` is unknown, a rule whose region is not "all" still resolves, but with applicability "uncertain" and `site.region` in its applicability facts. A Perth-and-Peel rule and its regional twin are now both reported "if it applies" instead of both able to report a plain MEETS.
- Applicability facts on every row (`core/evaluate.evaluate_rule`): the applicability facts are merged into `missing` for CANNOT_TELL as well as MEETS and DOES_NOT_MEET, and recorded as a note on NOT_APPLICABLE rows.
- Source hints (`core/evaluate.SOURCE_HINTS`): adjoining.*, overshadow.*, privacy.*, site_works.*, outbuilding.*, subdivision.* and ancillary.* are routed to named documents instead of "unknown source".
- No provision beats a missing value (`core/evaluators.ev_threshold`, `ev_count`, `ev_percentage_of`, `ev_formula`): a threshold that resolves to a null table row gives NOT_APPLICABLE even when the tested fact is unknown, as `ev_table_lookup` already did. An unknown threshold (key fact missing) still gives CANNOT_TELL.
- Chapter 1 (`chapters/ch1/operation.applicability`): the note on the "all codings" rows of Table 1.1 (single house, grouped dwelling), which is about R100, R160 and LR/MR/HR, is printed, prefixed "Note:", only for those codings; it no longer appears for an R20 lot. The data file is unchanged.
- Worked example: plan-only C3.4.1#rear-r17.5 is now Not applicable (was Cannot tell); counts 9 Meets, 1 Not applicable, 78 Cannot tell, 12 Not evaluated. C2.3.1, C2.3.2, C2.3.3 and C2.3.4 now carry `site.region`. Scenario statuses are unchanged; its missing-facts groups gain the new sources. Reports regenerated; tests in `tests/test_engine.py` and `tests/test_worked.py`.
- Also (`core/evaluators.safe_eval`): formula fact names are read in sorted order, so the missing-facts order in a report no longer varies between runs.

## 2026-11-06 Open items from a private run on a real R5 construction set (not published)

Rule and engine items to fix in pass 2; none changes a verified value.

- C3.9.3 (narrow adjoining lot): should be NOT_APPLICABLE when the adjoining lot is coded below R40 instead of asking for its frontage and battleaxe status; the C3.9.2 single-storey exemption was not applied on the run.
- C3.4.4(ii), (iii), #r1, #r2 and C3.4.5 (judgment records): need the "at least one boundary wall" condition C3.4.4(i) carries, so they drop out when no boundary wall is proposed.
- C4.1.2, C4.1.3, M4.1.2, M4.1.5: should carry a subdivision.proposed condition; C4.1.1 reports MEETS where its own note says the existing-lot exception makes it not applicable.
- C2.6.1 provisos (setback, site cover, landscaping) are not tested for the outbuilding itself: the C3.4.1 rules read the dwelling's setbacks only, so an outbuilding closer to a boundary than the dwelling passes silently. Needs outbuilding setback facts.
- C3.5.2: add a "retaining present" condition so a design with no retaining walls is not CANNOT_TELL.
- C3.6.4: carport width rule runs for a carport behind the setback line (already flagged on the record).
- Report display: C3.3.2(i)#r1 prints permitted width as tested and built width as threshold (reads backwards); C3.3.2(ii) prints twice the projection as tested.
- Report counts omit provisions excluded by coding or conditions; add an "excluded" count.
- Finding on the draft itself: the deletion of the averaging and area-compensation devices (register ch2-047) bites on designs drawn to the current code; under the draft only Table 3.3b's reduced portion (8 m at R5 for up to the greater of 30% of frontage or 4 m) and the C3.3.2(ii) porch, verandah or equivalent projection remain, and whether an alfresco counts as "verandah or equivalent" decides the outcome.
