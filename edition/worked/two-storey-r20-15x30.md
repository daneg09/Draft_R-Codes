# Draft R-Codes assessment: a two-storey project home on a 15 m x 30 m R20 lot

Draft R-Codes draft-2026-10-24 (consultation draft, not in force; consultation closes 26 February 2027; the PDF governs).
Worked example of `SKILL.md` Mode 1. Clause IDs are short forms of `rcodes:draft-2026-10-24/ch2/<clause>`.

## The brief and the plan

Brief (owner): "the design on an R20 lot with the following dimensions: 15m wide, 30m deep." No lot number, street, LGA, region or orientation.

Plan: a two-storey project home design supplied by the owner as a single marketing page; cited below as the plan page supplied by the owner (not published). It shows the ground and upper floor plans with room sizes, overall length 20.390 m and width 10.100 m, a double garage 5610 x 5710 internal, alfresco 4500 x 3300, 5 bedrooms, 3 bathrooms, a 12.5 m minimum lot width printed on the plan (a note only; not read by any rule), and a front elevation render (not a measured drawing).

It does not show: a site plan, setbacks, north point, verge or footpath, levels or heights, driveway, fences, landscaping, trees, outbuildings, bins or services, or anything about the adjoining lots. Every fact below was read by the assessor from the page or the brief; none was supplied by an applicant.

## Facts (plan-only file `examples/two-storey-r20-15x30-plan-only.json`)

| Fact | Value | Method | Conf. | Source and basis |
|---|---|---|---|---|
| site.r_code | R20 | stated | 1.0 | brief |
| site.width_m / depth_m | 15 / 30 | stated | 1.0 | brief |
| site.area_m2 | 450 | computed | 1.0 | 15 x 30; rectangular lot, no truncation |
| site.frontage_m | 15 | assumed | 0.9 | taken as equal to the width; the brief does not say which side faces the street |
| proposal.dwelling_type / dwelling_count | single_house / 1 | inferred | 1.0 | one dwelling on the page |
| proposal.storeys, building.storeys | 2 | inferred | 1.0 | two floor plans, two-storey render |
| proposal.bedrooms | 5 | stated | 1.0 | page summary; GUEST + BED 3, 4, 5 + MASTER SUITE |
| proposal.ancillary_dwelling | false | inferred | 0.95 | no second kitchen or unit |
| proposal.primary_living_space_floor | ground | inferred | 0.95 | FAMILY/DINING/KITCHEN on the ground floor |
| proposal.small_dwelling | false | inferred | 0.95 | 5-bed house, far above 70 m2 |
| proposal.seeks_universal_design_site_area_variation | false | inferred | 0.9 | brief: one house on an existing lot |
| subdivision.proposed | false | inferred | 0.9 | brief: no lots created |
| building.roofed_area_m2 | 193 | measured | 0.85 | ground outline scaled at ~34 px/m, including alfresco (taken as under the main roof) and porch, excluding eaves; +/- 5 m2. The 20.39 x 10.10 = 205.9 m2 box is an upper bound (rear and left side are narrower); without the alfresco ~178 m2 |
| building.house_length_m / house_width_m | 20.39 / 10.10 | stated | 1.0 | printed dimensions (not read by any rule) |
| building.upper_storey_wall_max_length_m | 12.3 | measured | 0.85 | upper floor scaled front to back, +/- 0.3 m |
| building.entrance_identifiable_from_street | true | inferred | 0.85 | render: entry beside the garage |
| building.major_opening_to_frontage | true | inferred | 0.85 | render: street-facing windows |
| parking.spaces | 2 | inferred | 0.9 | two garage bays; driveway not shown, so a minimum |
| parking.garage_carport_spaces | 2 | stated | 1.0 | page summary: 2 car spaces; garage drawn with two cars |
| parking.garage.present / bays | true / 2 | stated | 1.0 | GARAGE 5610 x 5710 (`bays` is not read by any rule) |
| parking.garage.ext_width_m | 5.83 | computed | 0.8 | 5.61 + 2 x 0.11 m single-leaf wall allowance (scaled ~5.78 m; double brick would give 6.15 m) |
| parking.garage.parallel_parking | false | inferred | 0.95 | door faces the street |
| parking.garage.upper_floor_over_half_width, entrance_clearly_visible | true, true | inferred | 0.85 | render and upper plan |
| parking.carport.present | false | inferred | 0.85 | parking is the enclosed garage |

## Plan-only assessment

Chapter: ch2 (Table 1.1, single house at R20). Pathway: **undetermined**. DA (Figure 2.1): not required if all deemed-exempt provisions are met; `site.scheme_requires_da` unknown. Engine counts: 9 Meets, 1 Not applicable, 78 Cannot tell, 12 Not evaluated.

| Element | Clause ID | Outcome | Value tested | Threshold | Exception or variation used | Page |
|---|---|---|---|---|---|---|
| 2.3 Parking | ch2 C2.3.3 ⚑ | Meets, if it applies (regional only; region unknown) | 2 | >= 2 (Table 2.3b, 3+ bed) | none | p19 |
| 3.1 Site cover | ch2 C3.1.1 | Meets | 42.9% (193/450) | <= 55% | none; the 205.9 m2 upper bound (45.8%) also meets | p27 |
| 3.2 Building height | ch2 C3.2.1#storeys | Meets | 2 storeys | <= 2 | none | p28 |
| 3.4 Lot boundary setbacks | ch2 C3.4.1#rear-r17.5 ⚑ | Not applicable | not shown | no provision at R20 | none | p32 |
| 3.4 Lot boundary setbacks | ch2 C3.4.2 | Meets | 12.3 m | <= 14 m | none | p33 |
| 3.6 Streetscape | ch2 C3.6.1 | Meets (render-inferred, 0.85) | entry and opening face street | yes | none | p37 |
| 3.6 Streetscape | ch2 C3.6.3 ⚑ | Meets | 38.9% (5.83/15) | <= 50% | none needed (60% exception not relied on) | p37 |
| 4.1 Site area | ch2 C4.1.1 ⚑ | Meets | 450 m2 | >= 350 m2 (Table 2B) | none | p49 |
| 4.1 Site area | ch2 C4.1.1-r3 | Meets | 15 m | >= 10 m (Table 2B) | none | p51 |
| 4.1 Site area | ch2 C4.1.1-r2 ⚑ | Meets, if it applies (site.battleaxe unknown) | 450 m2 | >= 450 m2 | none | p51 |

Cannot tell (78): 1.1 C1.1.1, -r1, -r2, -r3, C1.1.2; 1.2 C1.2.1, -r1, C1.2.2, C1.2.3, -r1, -r2, C1.2.5; 1.3 C1.3.1; 2.1 C2.1.1(i); 2.3 C2.3.1, C2.3.2, C2.3.4; 2.4 C2.4.1; 2.5 C2.5.1, C2.5.2; 2.6 C2.6.1, -r1; 3.2 C3.2.1#height; 3.3 all 13 street setback rows; 3.4 C3.4.1 (three side bands, minor projections), C3.4.3, C3.4.4 (count, height, length, (i)); 3.5 C3.5.1-3; 3.6 C3.6.2, C3.6.5(i), (ii), C3.6.6-r1, -r2; 3.7 thirteen access rows; 3.9 C3.9.1, -diagonal, C3.9.3, C3.9.4; 3.10 eight privacy rows. Not evaluated (judgment, 12): C3.4.4(ii), (iii), #r1, #r2, C3.4.5, C3.7.10, C3.8.1, C4.1.2, C4.1.3, M4.1.2, M4.1.3, M4.1.5.

Elements on merit: none (nothing is "does not meet"; the pathway is undetermined, not deemed-exempt).

### Missing facts, by source, with the question to ask

- Lot plan or title: which side is the street, and is it a corner, battleaxe or laneway lot (`site.has_secondary_street`, `site.has_row`, `site.battleaxe`)? Region and parking Location A or B (`site.region`, `site.location`)? NCC climate zone (`site.climate_zone`)? Any significant tree to retain (`site.significant_tree_retained`)?
- Site plan: primary street, side and rear setbacks of the dwelling and garage (`building.primary_street_setback_m`, `building.side_setback_walls_*`, `building.rear_setback_m`, `parking.garage.setback_primary_m`); eaves projection into the setbacks; driveway widths, sightlines and forward-gear exit (3.7); AS2890.1 compliance (C2.3.2 or C2.3.4); bins and service utilities (2.4, 2.5).
- Elevations and levels: total building height and wall heights at each side boundary (`building.total_height_m`, `building.has_walls_*`).
- Site works plan: levels, fill, excavation and retaining (3.5, `site_works.*`).
- Site plan, outbuildings: whether there is one, its area, wall and ridge height (2.6, `outbuilding.*`).
- Landscape plan: outdoor living area size, dimension and roof cover (1.1); soft landscaping, street setback soft area, trees and deep soil (1.2); stormwater (1.3); front fence (3.6); access from family room to the garden (C2.1.1(i)).
- Adjoining lot information: the neighbours' codings, frontages and whether they are vacant (`adjoining.*`).
- Shadow diagram: overshadowing at midday 21 June (3.9, `overshadow.*`).
- Elevations and site plan, cone of vision: setbacks from upper bedrooms and the activity room (3.10, `privacy.*`).
- Civil design: footpath or road offset from the street boundary (`site.verge.path_or_road_offset_m`).
- Application form: whether the scheme requires a DA anyway (`site.scheme_requires_da`).

## The scenario (`examples/two-storey-r20-15x30-scenario.json`)

A declared siting, not a site plan. Each fact is `method: assumed`, confidence 1.0, noted "scenario assumption"; the engine treats them as given, so every result below is conditional on them.

- Regional (South West), outside Perth and Peel; parking Location B; NCC climate zone 5.
- Street on the 15 m side; no laneway, secondary street or communal street; not a battleaxe lot; no pedestrian access leg; vehicle access from the primary street.
- No LDP or LPP; the scheme does not itself require a DA.
- House centred on the frontage: garage side 1.5 m, other side 3.4 m (1.5 + 10.10 + 3.4 = 15.0 m). Upper-floor walls on the garage side on the same 1.5 m line (upper plan ~9.9 m wide). Wall heights stay unknown.
- Front setback 6.0 m to the dwelling and the garage (garage flush with the porch line); no portion built forward, no porch projection.
- Rear setback 30 - 6.0 - 20.39 = 3.61 m.
- No boundary walls, no boundary carport or patio, no front fence.
- Soft landscaping, trees, OLA, levels, heights, driveway, privacy and overshadowing left unknown.

## Scenario assessment

Pathway: **undetermined**. DA (Figure 2.1): not required if all deemed-exempt provisions are met. Engine counts: 15 Meets, 1 Not applicable, 48 Cannot tell, 11 Not evaluated.

| Element | Clause ID | Outcome | Value tested | Threshold | Exception or variation used | Page |
|---|---|---|---|---|---|---|
| 1.1 Private open space | ch2 C1.1.2 | Meets, if it applies (OLA location unknown) | no front fence | fences visually permeable or none | none | p9 |
| 2.3 Parking | ch2 C2.3.3 ⚑ | Meets | 2 | >= 2 (Table 2.3b, 3+ bed) | none | p19 |
| 3.1 Site cover | ch2 C3.1.1 | Meets | 42.9% | <= 55% | none | p27 |
| 3.2 Building height | ch2 C3.2.1#storeys | Meets | 2 | <= 2 | none | p28 |
| 3.3 Street setbacks | ch2 C3.3.1 | Meets | 6.0 m | >= 6.0 m (Table 3.3a, R15-R25) | none | p29 |
| 3.3 Street setbacks | ch2 C3.3.2(iii) | Meets, if it applies (corner-lot subdivision unknown) | 6.0 m | >= 2.5 m | none | p30 |
| 3.3 Street setbacks | ch2 C3.3.3 | Meets | 6.0 m | >= 5.0 m (Table 3.3c) | none | p31 |
| 3.4 Lot boundary setbacks | ch2 C3.4.1#side-to-3.5m | Meets, if it applies | 1.5 m | >= 1.0 m | none | p32 |
| 3.4 Lot boundary setbacks | ch2 C3.4.1#side-3.6-to-7m ⚑ | Meets, if it applies (no margin) | 1.5 m | >= 1.5 m | none | p32 |
| 3.4 Lot boundary setbacks | ch2 C3.4.1#rear-r17.5 ⚑ | Not applicable | 3.61 m | no provision at R20 | none | p32 |
| 3.4 Lot boundary setbacks | ch2 C3.4.2 | Meets | 12.3 m | <= 14 m | none | p33 |
| 3.4 Lot boundary setbacks | ch2 C3.4.4#count-r20-r25 | Meets | 0 | <= 2 | none | p34 |
| 3.6 Streetscape | ch2 C3.6.1 | Meets | yes | yes | none | p37 |
| 3.6 Streetscape | ch2 C3.6.3 ⚑ | Meets | 38.9% | <= 50% | none | p37 |
| 4.1 Site area | ch2 C4.1.1 ⚑ | Meets | 450 m2 | >= 350 m2 | none | p49 |
| 4.1 Site area | ch2 C4.1.1-r3 | Meets | 15 m | >= 10 m | none | p51 |

Cannot tell (48): 1.1 C1.1.1, -r1, -r2, -r3; 1.2 all seven; 1.3 C1.3.1; 2.1 C2.1.1(i); 2.3 C2.3.4; 2.4 C2.4.1; 2.5 C2.5.1, C2.5.2; 2.6 C2.6.1, -r1; 3.2 C3.2.1#height; 3.3 C3.3.1#r1, C3.3.2(iii)#r1; 3.4 C3.4.1(i), C3.4.1#side-over-7.1m; 3.5 C3.5.1-3; 3.6 C3.6.2; 3.7 C3.7.3(i)-(vi), C3.7.4, C3.7.5; 3.9 four rows; 3.10 eight rows. Not evaluated: the 11 judgment rows above less C3.7.10.

Elements on merit: none.

Fallbacks (the route if a pending provision is found not met; not assessed here): 1.1 M1.1, 1.2 M1.2, 1.3 M1.3, 2.1 M2.1, 2.3 M2.3, 2.4 M2.4, 2.5 M2.5, 2.6 M2.6, 3.2 M3.2, 3.3 M3.3, 3.4 M3.4, 3.5 M3.5, 3.6 M3.6, 3.7 M3.7, 3.9 M3.9, 3.10 M3.10. The most likely candidate is 3.4: if any garage-side wall is taller than 7.1 m, the 1.5 m setback fails the 2.0 m of C3.4.1#side-over-7.1m and goes to M3.4.

### Draft ambiguities encountered

- C3.4.1#rear-r17.5 (p32, register ch2-055): Table 3.4a prints the rear 3 m as "applicable to R5-R15 only" and Table 2A prints N/A for R17.5 and above; the page does not say whether R20 has no rear setback or falls back to the side values. The 3.61 m rear setback is therefore untested. Under the side values it would meet 1.0/1.5 m, and 2.0 m above 7.1 m.
- C3.4.1 side bands (p32): bands are printed "up to 3.5m", "3.6m to 7m", "above 7.1m", leaving 3.5-3.6 m and 7.0-7.1 m undefined; the encoded split (> 3.5, > 7.0) is an inference. The garage side sits exactly on 1.5 m.
- C3.6.3 (p37): the clause says "upper floor balcony" but Figure 3.6a says "upper floor or balcony". Not decisive here: 38.9% passes the 50% base test.
- C2.3.3, Table 2.3b (p19): the second column is headed "Maximum ... R50 and above" but reads like minimums. The R40-and-below minimum of 2 used here is clear.
- C4.1.1 (p49): how C4.1.7(ii)'s 50% cap applies to a single lot is not stated. Not engaged: no small-dwelling or gold-level reduction is used.

## Summary

On a 15 m x 30 m R20 lot the design fits the numbers the plan itself fixes. Site cover is about 43% against 55% (46% even on the bounding box). The garage is about 39% of the frontage against 50%. It is two storeys, the upper walls are about 12.3 m long against 14 m, and the 450 m2 lot and 15 m frontage meet Table 2B. The house is 10.10 m wide, which leaves 4.9 m of side setback to share. With the declared siting (6.0 m front, garage side 1.5 m, other side 3.4 m, 3.61 m rear, regional Location B) the street setbacks, garage setback, ground and mid-height side setbacks, boundary walls and parking all meet. The 1.5 m garage side has no margin for walls 3.6 m to 7 m high, and fails if any wall on that side exceeds 7.1 m. Nothing has been found not met, but the pathway stays undetermined, so the design cannot yet be called deemed-exempt (no DA under Figure 2.1). To change that, the applicant must supply a site plan with setbacks, eaves, driveway, sightlines, bins and services; elevations with wall and building heights and levels; a landscape plan (outdoor living area, 15% soft landscaping, street setback landscaping, trees and deep soil, stormwater); shadow and cone-of-vision diagrams with the neighbours' codings; and the lot facts (region, Location, climate zone, orientation, verge). The rear setback question at R20 is a gap in the draft itself (ch2-055) and should be raised in a consultation submission. The draft is not in force.

## How to reproduce

From the repository root:

```
PYTHONPATH=src python -m rcodes applicability examples/two-storey-r20-15x30-plan-only.json
PYTHONPATH=src python -m rcodes run examples/two-storey-r20-15x30-plan-only.json --md
PYTHONPATH=src python -m rcodes run examples/two-storey-r20-15x30-scenario.json --md
```

Full engine output: `two-storey-r20-15x30-plan-only.report.json` and `two-storey-r20-15x30-scenario.report.json` beside this file. `tests/test_worked.py` keeps the outcomes above pinned to the rules.
