# Chapter 2 fact vocabulary

Dotted names as they appear in an application data document and in rule `inputs`.
Units: metres, square metres, percent (0 to 100), counts, booleans. A fact the applicant
cannot supply is simply absent; the engine then reports CANNOT_TELL and names it.

## site (lot plan, title, scheme map, civil design)

| Fact | Type | Meaning |
|---|---|---|
| site.r_code | code | R-coding of the lot |
| site.region | perth-peel / regional | Perth and Peel regions per Chapter 1 2.5.2 |
| site.climate_zone | int | NCC climate zone (4, 5, 6 trigger overshadowing) |
| site.area_m2 | number | site area |
| site.width_m, site.depth_m | number | nominal lot dimensions |
| site.frontage_m | number | frontage measured at the primary street setback line (A1 definition) |
| site.corner_lot | bool | |
| site.corner_lot_subdivided | bool | lot results from subdivision of an original corner lot (C3.3.2(iii)) |
| site.primary_street_class | enum | local, access, neighbourhood_connector, district_distributor, primary_distributor, integrator_arterial |
| site.has_secondary_street | bool | |
| site.has_row | bool | lot has frontage to a right-of-way or laneway |
| site.row_is_primary_street | bool | the laneway/ROW is the primary street |
| site.has_communal_street | bool | |
| site.access_from_rear_row | bool | vehicle access is taken from a rear right-of-way |
| site.battleaxe | bool | lot is a battleaxe lot |
| site.battleaxe_leg_width_m | number | |
| site.pedestrian_access_leg_width_m | number | |
| site.adjoining_pedestrian_access_way_width_m | number | width of an adjoining pedestrian access way (C3.4.1(ii)) |
| site.verge.path_or_road_offset_m | number | existing or planned footpath, shared path or road alignment distance from street boundary |
| site.road_widening_m | number | road widening requirement on the frontage |
| site.location | A / B | parking Location A or B (Table 2.3a note) |
| site.adjoins_public_open_space | bool | |
| site.scheme_requires_da | bool | |
| site.heritage_or_special_control | bool | |
| site.instruments | list | local instruments (instrument.schema.json) |
| site.significant_tree_retained | bool | a significant existing tree is retained (C1.2.4) |
| site.retained_tree_root_zone_provided | bool | nominal root zone per AS4970 (C1.2.5) |
| site.lot_approved_by_wapc | bool | the lot, survey-strata lot or strata lot was approved by the WAPC at its current area (C4.1.4(i)) |
| site.existing_lot_with_legal_access | bool | existing lot, survey-strata lot or strata lot with permanent legal access to a public road (C4.1.4(ii)) |
| site.structure_plan_or_ldp_approved_before_2024_04_10 | bool | lot is within a structure plan and/or local development plan approved before 10 April 2024 (C2.2.2 transitional footnote, until 10 April 2030) |
| site.has_pedestrian_access_leg | bool | a pedestrian access leg is required (C3.7.8) |
| site.pedestrian_access_leg_clear_path_m | number | continuous path of travel in the pedestrian access leg clear of utilities and minor projections, eaves excluded (C3.7.8(ii)) |

## adjoining (neighbouring lots, for overshadowing and privacy)

| Fact | Type | Meaning |
|---|---|---|
| adjoining.south.r_code | code | coding of the lot that receives the shadow |
| adjoining.south.frontage_m | number | |
| adjoining.south.is_grouped_site | bool | adjoining site is a grouped-dwelling site |
| adjoining.south.existing_dwelling | bool | |
| adjoining.diagonal.r_code | code | diagonally adjacent lot receiving shadow |
| adjoining.north_shared_boundary_count | int | number of lots sharing the northern boundary (C3.9.4) |
| adjoining.vacant_or_unknown | bool | adjoining site vacant or dwelling layout unknown (C3.10.4) |
| adjoining.south.battleaxe | bool | the adjoining southern lot is a battleaxe lot (C3.9.3(ii)) |
| adjoining.all_coded_r100_sl | bool | every adjoining property is coded R100-SL (Table 2.10a footnote 1) |

## proposal

| Fact | Type | Meaning |
|---|---|---|
| proposal.dwelling_type | single_house | |
| proposal.storeys | int | storeys of the dwelling |
| proposal.bedrooms | int | 0 for studio |
| proposal.internal_floor_area_m2 | number | |
| proposal.ancillary_dwelling | bool | proposal includes an ancillary dwelling |
| proposal.small_dwelling | bool | dwelling is a small dwelling (C2.9.1) |
| proposal.retained_dwelling | bool | an existing dwelling is retained (3.8) |
| proposal.universal_design_level | none / silver / gold | A4 or Livable Housing Australia level |
| proposal.primary_living_space_floor | ground / upper | |
| proposal.mixed_use | bool | |
| proposal.seeks_universal_design_site_area_variation | bool | the application seeks the gold-level universal design site area variation under C4.1.6 or C4.1.7 (C2.7.1) |

## building (site plan, elevations)

| Fact | Type | Meaning |
|---|---|---|
| building.roofed_area_m2 | number | site cover area per the A1 definition (all buildings and roofed structures; excludes eaves, pergolas, uncovered driveways) |
| building.storeys | int | |
| building.total_height_m | number | maximum total building height above NGL |
| building.max_wall_height_m | number | highest wall (for the single-storey overshadowing exemption) |
| building.primary_street_setback_m | number | minimum setback of the dwelling to the primary street boundary |
| building.primary_street_setback_reduced_portion_m | number | setback of the portion built forward under C3.3.2(i) |
| building.primary_street_reduced_portion_width_m | number | width of frontage built forward |
| building.primary_street_projection_m | number | depth of minor projections into the setback (eaves, chimneys, hoods) |
| building.porch_projection_m | number | depth of porch, verandah or unenclosed balcony into the setback (C3.3.2(ii)) |
| building.porch_street_setback_m | number | absolute setback of a porch, balcony, verandah or equivalent to the street boundary (C3.3.2(iii)) |
| building.secondary_street_setback_m | number | |
| building.row_setback_m | number | setback to laneway or right-of-way |
| building.side_setback_walls_to_3_5m_m | number | minimum side setback of walls up to 3.5 m high |
| building.side_setback_walls_3_6_to_7m_m | number | minimum side setback of walls 3.6 to 7 m |
| building.side_setback_walls_over_7_1m_m | number | minimum side setback of walls above 7.1 m |
| building.has_walls_to_3_5m | bool | the building has walls up to 3.5 m high facing a side boundary; condition for the C3.4.1 to-3.5m side setback band rules |
| building.has_walls_3_6_to_7m | bool | the building has walls 3.6 m to 7 m high facing a side boundary; condition for the C3.4.1 3.6-to-7m band rules |
| building.has_walls_over_7_1m | bool | the building has walls 7.1 m high or more facing a side boundary; condition for the C3.4.1 over-7.1m band rules |
| building.rear_setback_m | number | |
| building.side_projection_m | number | minor projections into side setbacks |
| building.upper_storey_wall_max_length_m | number | longest second or third storey wall including balconies (C3.4.2) |
| building.upper_storey_wall_over_14m_setback_m | number | setback of the portion beyond 14 m |
| building.upper_storey_wall_has_3x3_separation | bool | 3 m x 3 m separation instead (C3.4.2) |
| building.boundary_walls.count | int | number of lot boundaries with boundary walls |
| building.boundary_walls.max_height_m | number | includes any retaining wall beneath (C3.4.5) |
| building.boundary_walls.max_length_m | number | longest boundary wall |
| building.boundary_walls.max_pct_of_boundary | number | longest wall as % of the boundary it abuts |
| building.boundary_walls.excl_adjoining_pos_pct | number | as above excluding portions abutting adjoining POS (narrow lots, Table 3.4c) |
| building.boundary_walls.behind_street_setback | bool | |
| building.boundary_walls.beyond_14m_setback_m | number | R50+: setback of the portion beyond 14 m |
| building.boundary_walls.beyond_14m_setback_length_m | number | R50+: length of that set-back portion |
| building.boundary_walls.adjoining_wall_exists | bool | abuts an existing or simultaneously built wall of similar or greater size (C3.4.5) |
| building.boundary_structure.present | bool | a carport, patio, verandah or equivalent is built up to a lot boundary (C3.4.3) |
| building.boundary_structure.length_m | number | carport, patio, verandah on the boundary (Table 3.4b) |
| building.boundary_structure.post_height_m | number | |
| building.boundary_structure.ridge_height_m | number | |
| building.boundary_structure.post_size_mm | number | largest horizontal dimension of pillars or posts |
| building.addresses_street | bool | primary entrance identifiable and a major opening to the frontage (C3.6.1) |
| building.fronts_street_or_row | bool | dwelling fronts a primary street, secondary street or public right-of-way (C2.10.1(i)) |
| building.entrance_identifiable_from_street | bool | |
| building.major_opening_to_frontage | bool | |
| building.upper_level_outlook_to_pos | bool | upper-level balcony or habitable-room window overlooking adjoining POS (C3.6.2) |
| building.front_fence.height_m | number | fence or wall in the primary street setback area |
| building.front_fence.permeable_above_m | number | height above which it is visually permeable |
| building.front_fence.pillar_height_m | number | |
| building.front_fence.pillar_size_mm | number | |
| building.front_fence.present | bool | a street wall or fence is provided in the primary street setback area (C3.6.5) |
| building.front_fence.pillars_present | bool | the fence includes solid pillars (C3.6.6) |
| building.front_fence.visually_permeable | bool | street walls and fences in the primary street setback area are visually permeable per C3.6.5 and C3.6.6, or there are none (C1.1.2, C1.1.5) |
| building.courtyard_daylight_only | bool | a courtyard is the sole daylight source to a habitable room (C2.2.1) |
| building.courtyard_area_m2 | number | |
| building.courtyard_open_to_sky | bool | the courtyard is uncovered and open to the sky, minor projections excluded (C2.2.1) |
| building.primary_living_major_opening_orientation | enum | NW, N, NE, E, other (C2.2.2) |
| building.primary_living_uncovered_area_m2 | number | uncovered area adjoining that opening |
| building.primary_living_uncovered_min_dim_m | number | |
| building.primary_living_direct_access_to_pga | bool | C2.1.1(i) |
| building.primary_living_direct_access_to_upper_pos | bool | upper-floor primary living space has direct physical and visual access to the balcony, rooftop terrace or public open space (C2.1.1(ii)) |
| building.upper_pos.area_m2 | number | balcony or rooftop terrace serving an upper-floor primary living space (Table 2.1a) |
| building.upper_pos.min_dim_m | number | |
| building.storage.area_m2 | number | Table 2.1b storage |
| building.storage.min_dim_m | number | |
| building.storage.height_m | number | |
| building.storage.behind_street_setback | bool | |

## site_works (3.5)

| Fact | Type | Meaning |
|---|---|---|
| site_works.forward_of_setback_max_change_m | number | max fill or excavation forward of the street setback line |
| site_works.forward_of_setback_for_access_drainage_light | bool | the change is for access, drainage or natural light |
| site_works.retaining_max_height_m | number | retaining wall or fill height behind the setback line |
| site_works.retaining_setback_m | number | its setback from the lot boundary |
| site_works.excavation_behind_setback | bool | |

## outbuilding (2.6)

| Fact | Type | Meaning |
|---|---|---|
| outbuilding.present | bool | |
| outbuilding.total_area_m2 | number | individual or collective area per site |
| outbuilding.wall_height_m | number | |
| outbuilding.ridge_height_m | number | |
| outbuilding.in_street_setback_area | bool | primary or secondary street setback area |
| outbuilding.matches_dwelling_materials | bool | external wall and roof materials and colour match (C2.6.2) |

## ancillary (2.8)

| Fact | Type | Meaning |
|---|---|---|
| ancillary.count | int | ancillary dwellings on the site |
| ancillary.internal_floor_area_m2 | number | |
| ancillary.on_same_site_as_small_dwelling | bool | |

## landscape (landscape plan)

| Fact | Type | Meaning |
|---|---|---|
| landscape.soft_area_m2 | number | soft landscape area per the A1 definition |
| landscape.soft_min_dim_m | number | |
| landscape.street_setback_area_m2 | number | area of the primary street setback area |
| landscape.street_setback_soft_area_m2 | number | soft landscape within it |
| landscape.trees_in_street_setback | int | small trees in the primary street setback area |
| landscape.trees_elsewhere | int | small trees elsewhere on the lot |
| landscape.tree_deep_soil_min_m2 | number | smallest deep soil area provided to any required tree |
| landscape.tree_deep_soil_min_dim_m | number | |
| landscape.ola.area_m2 | number | outdoor living area (R2-R40) |
| landscape.ola.min_dim_m | number | |
| landscape.ola.behind_street_setback | bool | |
| landscape.ola.in_primary_street_setback | bool | consolidated OLA in the front setback (C1.1.2) |
| landscape.ola.uncovered_pct | number | % of the required OLA without permanent roof cover |
| landscape.pga.area_m2 | number | primary garden area (R50+) |
| landscape.pga.min_dim_m | number | |
| landscape.pga.behind_street_setback | bool | |
| landscape.pga.in_primary_street_setback | bool | C1.1.5 |
| landscape.pga.roofed_pct | number | % of PGA with permanent roof cover |
| landscape.secondary_pos.area_m2 | number | C1.1.4 secondary private open space |
| landscape.secondary_pos.min_dim_m | number | |
| landscape.secondary_pos.uncovered | bool | |
| landscape.secondary_pos.outside_street_setback | bool | |
| landscape.secondary_pos.extra_tree | bool | additional small tree provided |
| landscape.stormwater_retained_on_site | bool | runoff from a small rainfall event retained on site (C1.3.1) |
| landscape.stormwater_to_system_required | bool | decision-maker requires connection (C1.3.2) |

## parking (site plan)

| Fact | Type | Meaning |
|---|---|---|
| parking.spaces | int | on-site car parking spaces for the dwelling |
| parking.garage_carport_spaces | int | spaces within garages and carports |
| parking.ancillary_spaces | int | spaces for the ancillary dwelling |
| parking.ancillary_garage_carport_spaces | int | garage and carport spaces serving the ancillary dwelling (Tables 2.3a, 2.3b ancillary maximum) |
| parking.as2890_compliant | bool | spaces and manoeuvring per AS2890.1 |
| parking.garage.present | bool | |
| parking.garage.setback_primary_m | number | garage to the primary street boundary |
| parking.garage.setback_secondary_m | number | |
| parking.garage.setback_row_m | number | |
| parking.garage.ext_width_m | number | garage door and supporting structure width at the setback line |
| parking.garage.parallel_parking | bool | |
| parking.garage.parallel_wall_openings | int | |
| parking.garage.upper_floor_over_half_width | bool | upper floor or balcony over more than half the garage width (C3.6.3) |
| parking.garage.entrance_clearly_visible | bool | |
| parking.carport.present | bool | |
| parking.carport.setback_primary_m | number | |
| parking.carport.setback_secondary_m | number | |
| parking.carport.setback_row_m | number | carport setback to a laneway or right-of-way |
| parking.carport.width_m | number | including supporting structures |
| parking.carport.free_of_walls_forward_of_setback | bool | |
| parking.carport.post_size_mm | number | |
| parking.carport.unobstructed_view_dwelling_to_street | bool | |
| parking.access.count | int | vehicle access points to the lot |
| parking.access.from_lowest_order_street | bool | C3.7.1 |
| parking.access.street_type | enum | row, communal_street, secondary_street, primary_street |
| parking.driveway.width_min_m | number | |
| parking.driveway.width_at_boundary_m | number | |
| parking.driveway.aggregate_width_m | number | aggregate at street boundary (R35 and below) |
| parking.driveway.setback_to_corner_m | number | |
| parking.driveway.right_angle_to_carriageway | bool | |
| parking.driveway.trafficable_and_drained | bool | |
| parking.driveway.space_to_boundary_m | number | distance from a car space to the street boundary (C3.7.4) |
| parking.driveway.exit_forward_gear | bool | |
| parking.sightlines.clear_0_75m_within_1_5m | bool | nothing above 0.75 m within 1.5 m of the driveway at the boundary (C3.7.5) |
| parking.sightlines.row_truncation_1m | bool | C3.7.7 |

## services (2.4, 2.5)

| Fact | Type | Meaning |
|---|---|---|
| services.bins_screened | bool | |
| services.service_utilities_accessible_screened | bool | C2.5.1 |
| services.functional_utilities_behind_setback | bool | C2.5.2 |
| services.functional_utilities_not_visible_from_street | bool | |

## overshadow (shadow diagram, midday 21 June)

| Fact | Type | Meaning |
|---|---|---|
| overshadow.adjoining_pct | number | shadow cast on the adjoining property as % of its site area |
| overshadow.diagonal_pct | number | on the diagonally adjacent lot |
| overshadow.adjoining_rear_half_pct | number | shadow on the rear half of a narrow adjoining lot (Table 3.9b) |
| overshadow.proportional_to_shared_boundary | bool | C3.9.4 |

## privacy (cone of vision)

| Fact | Type | Meaning |
|---|---|---|
| privacy.sources_above_0_5m | bool | any major opening or active habitable space with floor level more than 0.5 m above NGL |
| privacy.bedroom_study_setback_m | number | minimum cone-of-vision setback from a bedroom or study major opening |
| privacy.bedroom_study_offset_m | number | edge-to-edge offset between a bedroom/study major opening and the parallel adjoining opening (C3.10.3) |
| privacy.other_habitable_setback_m | number | from other habitable room major openings |
| privacy.outdoor_active_setback_m | number | from outdoor active habitable spaces |
| privacy.cone_captures_adjoining_opening | bool | cone captures a major opening or active habitable space of an existing adjoining dwelling |
| privacy.cone_forward_of_adjoining_setback_line | bool | C3.10.2 |
| privacy.screened_or_offset | bool | fallback screening or 1.5 m offset (C3.10.3) |

## subdivision (4.1)

| Fact | Type | Meaning |
|---|---|---|
| subdivision.proposed | bool | the application creates lots |
| subdivision.lot_count | int | |
| subdivision.min_site_area_m2 | number | smallest proposed site area |
| subdivision.min_battleaxe_site_area_m2 | number | smallest proposed rear battleaxe lot area, calculated per C4.1.3(ii)-(iv) (Table 2B) |
| subdivision.avg_site_area_m2 | number | |
| subdivision.min_frontage_m | number | |
| subdivision.battleaxe_lot | bool | |
| subdivision.green_title_or_survey_strata | bool | |
| subdivision.reduced_lots_count | int | lots below the minimum |

## Usage notes

Readings of existing facts that rules rely on (carried from the authors' proposals):

- landscape.ola.uncovered_pct: percentage of the REQUIRED outdoor living area (Table 1.1a) without permanent roof cover (eaves excluded).
- landscape.pga.roofed_pct: percentage of the PGA PROVIDED with permanent roof cover (C1.1.3-r2); roofed_pct <= 0 encodes 'uncovered' for R100-SL.
- building.primary_street_setback_m: also the Table 1.2a trigger 'where the primary street setback is 1.5m or greater' (read as the setback provided; verify).
- subdivision.lot_count, subdivision.reduced_lots_count: drive the 50% caps in C4.1.6(ii) and C4.1.7(ii); supply 1 and 1 (or 0) for a single existing lot.
- site_works.excavation_behind_setback: read as 'all excavation on the site lies behind the street setback line' (C3.5.3); true where no excavation is proposed.
- privacy.screened_or_offset: also the C3.10.5 screening exception on the C3.10.4 rules, although C3.10.5 does not list the offset.
- site.access_from_rear_row: also the C3.7.7 trigger 'vehicle access is taken from a right-of-way' (a side ROW is not distinguished).

Chapter 3 readings (carried from the authors' part 1 to part 4 proposals):

- subdivision.site_area_per_dwelling_m2: the SMALLEST dwelling site area in the development, calculated per C4.1.2(i) (dwelling plus exclusive-use areas, common property excluded) and adjusted per C4.1.3. Used by C4.1.1 and the 100 m2 floor of C4.1.6(i) and C4.1.7(i).
- subdivision.avg_site_area_per_dwelling_m2: average of those dwelling site areas (C4.1.1-r7).
- proposal.reduced_site_area_dwelling_count: used with proposal.dwelling_count for the 50% caps of C4.1.6(ii) and C4.1.7(ii) in C4.1.1 and C4.1.1-r7.
- parking.uncovered_at_grade_spaces, landscape.parking_shade_trees: C1.2.5 tests 4 x trees >= spaces (one small shade tree per four uncovered at-grade spaces, rounded up).
- landscape.trees_elsewhere, landscape.trees_in_street_setback: counts for the whole development lot; C1.2.4-r1 compares them with proposal.dwelling_count (one small tree per dwelling).
- site.area_m2 in element 1.1 (Table 1.1b, C1.1.4 161 m2 threshold) and 1.2 (C1.2.1 15% 'per site'): the site of the dwelling being assessed (A1 'site' for a grouped dwelling). Whether C1.2.1 is tested per dwelling or across the development is ambiguous (register ch3-009).
- site.area_m2, building.roofed_area_m2 (C3.1.1): for a grouped dwelling, the dwelling's own site (land it occupies plus all areas for its occupants' exclusive use, no share of common property; A1 'site', register ch3-043; C4.1.2(i)). Not the parent lot. Run C3.1.1 once per dwelling, or supply the dwelling with the highest site cover.
- site.lot_approved_by_wapc, site.existing_lot_with_legal_access on the C4.1.1 / C4.1.1-r7 exceptions: the dwelling's own lot, survey-strata lot or strata lot. A new grouped development on a parent lot should answer false; answering true for the parent lot would waive Table 3B.
- subdivision.lot_count, subdivision.reduced_lots_count on C4.1.1-r1 and -r4: count lots ("dwellings or sites") created by the subdivision.
- services.waste.communal_storage_area_m2: 0 where no communal waste storage area is provided; a value above 0 triggers C2.4.3 (C2.4.2 in the Chapter 3 text is bin screening).
- services.waste.collection_point_accessible: no rule uses it. The Chapter 3 text has no collection-point clause (register ch3-033: the Part B communal pick-up clause was not carried over).
- parking.visitor_spaces_marked_and_accessible: true only where every visitor bay is (i) marked and signposted for visitor use only, (ii) on common property, and (iii) connected to building entries by a continuous path of travel (C2.3.4, C2.3.8).
- parking.visitor_spaces: the number of visitor bays on site. C2.3.3 and C2.3.7 compare it with the Table 2.3a/2.3b ratio; C2.3.4 and C2.3.8 apply when it is 1 or more.
- proposal.dwelling_count: the number of grouped dwellings in the development, not counting ancillary dwellings. It is the "total number of dwellings" in the visitor ratios (C2.3.3, C2.3.7) and drives the 5-dwelling waste plan note (C2.4.3-r1) and the 10-dwelling universal design trigger (C2.7.1). Verify whether ancillary dwellings count.
- proposal.dwellings_universal_design_pct: percentage of all dwellings built to silver level or better (gold counts). For a whole number of dwellings, pct >= 20 is the same test as count >= 20% of dwellings rounded up (C2.7.1 footnote 1).
- Per-dwelling facts (proposal.bedrooms, parking.spaces, parking.garage_carport_spaces, building.storage.*, building.upper_pos.*, proposal.internal_floor_area_m2): each describes the dwelling being tested. Where a development has more than one dwelling type, supply the least compliant dwelling, or run one application per dwelling type.
- building.internal_boundary_treated_as_lot_boundary (C3.4.6): true when every C3.4.1 to C3.4.5 test (setbacks, upper-storey wall length, boundary structures and boundary walls) is met at each internal site boundary between grouped dwellings on the same lot, read as if it were a lot boundary. A single setback number (building.internal_boundary_setback_m) cannot express this, because the required setback depends on wall height and C3.4.4 allows nil-setback walls.
- site.communal_street_serves_lots: dwellings served for C3.7.11 (10 or more grouped dwellings), and potential strata or survey-strata lots each taking driveway access for C3.7.15 (20 or more).
- site.communal_street_width_m: also the battleaxe leg width for C3.7.13; Chapter 2's site.battleaxe_leg_width_m is not used in Chapter 3.
- site.communal_street_passing_bay: one answer for both C3.7.5 (passing points at least every 30 m, 5.5 m x 6.3 m) and C3.7.6 (5.5 m x 6.3 m simultaneous entry/exit at the street boundary).
- parking.driveway.dwellings_served: use instead of proposal.dwelling_count for the five-or-more trigger of C3.7.4(i) and C3.7.5, since each dwelling may have its own crossover.
- parking.pedestrian_access_width_m: the pedestrian path width, tested at 1 m (C3.7.11(i)) and 1.2 m within a 20+ lot communal street (C3.7.15(ii)).
- parking.pedestrian_access_separate: true where the path is clearly delineated from, or separate from, vehicle access (C3.7.11(ii)); limb (iii) is parking.pedestrian_path_continuous.
- parking.sightlines.row_truncation_1m: also the 1 m x 1 m truncation at a communal street driveway (C3.7.9).
- building.storeys: for the C3.9.2 exception, the tallest building on the lot, so a single-storey dwelling on the same lot as a two-storey building does not qualify.
- overshadow.adjoining_pct, overshadow.diagonal_pct: where the adjoining site is a grouped dwelling development, the percentage of each grouped dwelling site area excluding common property (Table 3.9a footnote 1).

## grouped (Chapter 3 only)

| Fact | Type | Meaning |
|---|---|---|
| proposal.dwelling_count | int | number of grouped dwellings on the site |
| proposal.dwellings_universal_design_pct | number | % of dwellings meeting silver level (C2.7.1) |
| proposal.reduced_site_area_dwelling_count | int | number of grouped dwellings whose site area relies on the C4.1.5 to C4.1.7 reduction (C4.1.6(ii), C4.1.7(ii) 50% caps) |
| site.common_property_area_m2 | number | common property area |
| site.has_communal_street | bool | (already in site; communal street serves the dwellings) |
| site.communal_street_width_m | number | communal street or battleaxe leg width (C3.7.13, C3.7.14) |
| site.communal_street_serves_lots | int | lots or dwellings the communal street serves (C3.7.15 threshold 20) |
| site.communal_street_landscaped_and_lit | bool | C1.2.3 |
| site.communal_street_passing_bay | bool | passing or simultaneous entry/exit provided (C3.7.5, C3.7.6) |
| site.communal_street_length_m | number | |
| site.communal_street_carriageway_width_m | number | paved vehicular carriageway width within the communal street (C3.7.15(i)) |
| site.communal_street_soft_landscape_width_m | number | width of soft landscaping within the communal street (C3.7.15(iii)) |
| building.communal_street_setback_m | number | setback of a dwelling to a communal street or battleaxe leg |
| building.internal_boundary_setback_m | number | setback to an internal site boundary between dwellings on the same lot (C3.4.6) |
| building.internal_boundary_treated_as_lot_boundary | bool | C3.4.6 |
| parking.visitor_spaces | int | visitor bays on common property (C2.3.3, C2.3.7) |
| parking.visitor_spaces_marked_and_accessible | bool | C2.3.4 |
| parking.uncovered_at_grade_spaces | int | number of uncovered at-grade car parking spaces on the site (C1.2.5) |
| parking.pedestrian_access_separate | bool | pedestrian access separate from vehicle access (C3.7.10 to C3.7.12) |
| parking.pedestrian_access_width_m | number | |
| parking.pedestrian_path_continuous | bool | the pedestrian path is a continuous path of travel from the street boundary to ground-floor dwelling or building entries (C3.7.11(iii)) |
| parking.driveway.side_boundary_setback_m | number | least clearance of any driveway to a side lot boundary or street pole (C3.7.3(iii)) |
| parking.driveway.dwellings_served | int | most dwellings served by any one driveway (C3.7.4(i), C3.7.5) |
| landscape.landscaping_plan_provided | bool | C1.2.8 |
| landscape.parking_shade_trees | int | small shade trees planted to serve the uncovered at-grade parking, additional to the C1.2.4 trees (C1.2.5) |
| services.waste.communal_storage_area_m2 | number | communal waste storage area; above 0 triggers C2.4.3 |
| services.waste.bin_space_per_lg_requirements | bool | a dedicated, accessible space holds the number and type of waste bins the local government requires for the dwelling (C2.4.1) |
| services.waste.communal_area_separated_or_screened | bool | the communal waste storage area is separated or screened from major openings, primary garden areas and communal open space (C2.4.3) |
| services.waste.collection_point_accessible | bool | C2.4.3 |
| subdivision.site_area_per_dwelling_m2 | number | site area per dwelling for Table 3B |
| subdivision.avg_site_area_per_dwelling_m2 | number | |
