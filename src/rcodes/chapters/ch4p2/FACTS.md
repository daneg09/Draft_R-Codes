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
| proposal.reduced_small_dwelling_count | int | of proposal.reduced_site_area_dwelling_count, how many are small dwellings (C2.9.1); C4.1.4 and the C4.1.6 50% cap count small dwellings only (C4.1.1) |

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
| ancillary.dual_key | bool | every ancillary dwelling is a dual key dwelling (Table 2.8a, dual key only) |

## landscape (landscape plan)

| Fact | Type | Meaning |
|---|---|---|
| landscape.soft_area_m2 | number | soft landscape area per the A1 definition |
| landscape.soft_min_dim_m | number | |
| landscape.street_setback_area_m2 | number | area of the primary street setback area |
| landscape.street_setback_soft_area_m2 | number | soft landscape within it |
| landscape.trees.small_count | int | small trees (Table 1.2b size) on the whole development lot, excluding C1.2.5 parking shade trees; a retained significant tree counts by its size (C1.2.4 to C1.2.4-r5, Table 1.2a) |
| landscape.trees.medium_count | int | medium trees, counted as for small_count |
| landscape.trees.large_count | int | large trees, counted as for small_count |
| landscape.deep_soil.small_min_m2 | number | smallest deep soil area given to any small tree (Table 1.2b, C1.2.4-r3) |
| landscape.deep_soil.small_min_dim_m | number | smallest deep soil dimension given to any small tree (C1.2.4-r3) |
| landscape.deep_soil.medium_min_m2 | number | smallest deep soil area given to any medium tree (C1.2.4-r4) |
| landscape.deep_soil.medium_min_dim_m | number | smallest deep soil dimension given to any medium tree (C1.2.4-r4) |
| landscape.deep_soil.large_min_m2 | number | smallest deep soil area given to any large tree (C1.2.4-r5) |
| landscape.deep_soil.large_min_dim_m | number | smallest deep soil dimension given to any large tree (C1.2.4-r5) |
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

Chapter 4 Part 1 readings (carried from the authors' part 1 to part 3b proposals):

- dwellings: the apartment facts are summary facts under an object (dwellings.min.*, dwellings.max.*, dwellings.*_pct); the application schema accepts dwellings as an object (summary facts) or an array (per-dwelling records).
- proposal.dwelling_count: the number of apartments in the development. Drives C1.3.1 (more than 10), C2.1.7 (more than 10), C2.3.3 (exceeding 20), the visitor and bicycle ratios (C2.3.5, C2.3.7, C2.3.7-r1), C2.7.1 (10 or more), Table 2.8a (1-19 / 20 or more), and is the C4.1.1 divisor. Verify whether ancillary (dual key) dwellings count.
- proposal.reduced_site_area_dwelling_count: apartments relying on a C4.1.4 to C4.1.6 35% reduction, each a small dwelling or (R30 and above) a gold-level universal design dwelling. Supply 0 where none; C4.1.1 then reads it in the C4.1.7 tree formula.
- subdivision.truncation_area_added_m2: corner truncation area claimed under C4.1.2; supply 0 where none. C4.1.1 adds min(value, 20) to site.area_m2.
- site.area_m2 in elements 1.2 and 4.1: the whole development lot (apartments have no individual sites). Table 1.2a 'lot size' is read as this.
- site.area_m2, building.roofed_area_m2 (C3.1.1): for apartments the whole lot, or parent lot under a strata scheme, on which the dwellings stand (Appendix A1 'SITE', multiple dwelling or apartment limb), not a per-dwelling site as in Chapter 3.
- site.retained_tree_root_zone_provided (C1.2.7): read as the AS4970 tree protection zone, which is what this chapter's text says.
- C4.1.7 tree reduction: the 10% is the code's value, not an applicant fact; the trigger is site.significant_tree_retained (this replaces subdivision.avg_site_area_reduction_tree_pct).
- landscape.trees.*, landscape.deep_soil.*: Table 1.2a here counts trees by Table 1.2b size, replacing the Chapter 3 small-trees-by-location counts (landscape.trees_in_street_setback, landscape.trees_elsewhere) and the single landscape.tree_deep_soil_min_m2 / tree_deep_soil_min_dim_m, which cannot express the size-dependent deep soil.
- landscape.cos.area_m2: 0 where no communal open space is provided; above 0 triggers C1.2.3-r1, C1.3.2, C1.3.3.
- dwellings.min.internal_floor_area_m2, dwellings.min.bedrooms_of_smallest (C2.1.6): the least compliant apartment is the one with the smallest margin over its own Table 2.1a requirement (a small studio can pass while a larger 3-bed fails), not necessarily the smallest. Supply that apartment, or run one application per apartment type.
- dwellings.min.storage_area_m2, dwellings.min.storage_min_dim_m, dwellings.min.storage_circulation_m: the same apartment as dwellings.min.storage_bedrooms. storage_circulation_m is the clear width of the circulation space adjacent to the store (C2.1.9(i), 0.9 m).
- dwellings.ground_floor_openings_to_car_park: trigger for C2.1.10, true where any ground-floor apartment has a major opening facing directly onto car parking areas or a non-residential component of a mixed use development.
- dwellings.max.single_aspect_living_depth_ratio: depth of the deepest single-aspect primary living space (excluding built-in cabinetry) divided by its ceiling height.
- dwellings.no_sun_pct (C2.2.2(ii)): per building; supply the building with the highest share.
- parking.resident_spaces: resident bays for the whole development (C2.3.1; Table 2.3a has no minimum).
- parking.resident_spaces_per_dwelling_avg: all occupant bays of every type (garage, carport, open, undercroft, basement) divided by the number of dwellings in the residential component (C2.3.4).
- parking.visitor_spaces: visitor bays on site (C2.3.5); also the trigger for C2.3.6 (1 or more).
- parking.visitor_bays_signed_common_property: read as covering all of C2.3.6 (i) marked and signposted for visitors only, (ii) on common property and (iii) connected to building entries by a continuous path of travel.
- parking.bicycle_spaces, parking.bicycle_spaces_visitor: resident and visitor bicycle spaces (C2.3.7, C2.3.7-r1).
- proposal.seeks_universal_design_site_area_variation: in this chapter the variation is under C4.1.5 or C4.1.6 (the proposal section row above cites C4.1.6 or C4.1.7, the Chapter 3 numbers).
- proposal.internal_floor_area_m2: in C2.7.2 the accessible dwelling seeking the variation; in C2.9.1 the small dwelling under the concession.
- services.waste.bin_space_per_lg_requirements, services.waste.communal_storage_area_m2, services.waste.communal_area_separated_or_screened, services.bins_screened: as in Chapter 3 (C2.4.1 to C2.4.3).
- building.separation_same_lot_m (C3.4.6): the least separation between the facing walls, measured as for a lot boundary setback (minor projections up to 0.75 m excluded, C3.4.1(i)).
- building.upper_level_overlook_street (C3.6.1): true when upper-level balconies and/or windows overlook the street and public domain areas. The rule applies only where building.storeys >= 2. The public open space limb is C3.6.1-r1, which uses building.upper_level_outlook_to_pos where site.adjoins_public_open_space.
- building.storeys (C3.6.1, C3.6.1-r1): the storeys of the apartment building, not of one apartment (Chapter 3 used proposal.storeys per dwelling).
- building.ground_floor_apartments_separate_entry (C3.6.2): true where every ground-floor apartment fronting the street has its own pedestrian access from the street, and also true where no ground-floor apartment fronts the street.
- parking.path_of_travel_to_entries (C3.7.10): a legible, well-defined, continuous path from the public footpath and car parking areas to lobbies, stairs, accessways and individual dwelling entries.
- privacy.between_apartments_same_lot_compliant (C3.9.4): every source of overlooking between apartments on the same lot meets C3.9.1, C3.9.2 and C3.9.3, read as if the other apartment were on an adjoining property.
- proposal.retained_dwelling (C3.7.2(i) exception, C3.7.12(i) reduction): an existing dwelling is retained on the site. This chapter has no retained-dwelling element, but those two clauses still refer to retaining an existing dwelling.
- parking.driveway.dwellings_served (C3.7.4, C3.7.5): the number of apartments the driveway serves.
- site.communal_street_serves_lots: not used in this chapter. C3.7.11 has no 10-dwelling threshold and there is no 20-lot communal street clause.
- overshadow.adjoining_pct, overshadow.diagonal_pct (C3.8.1): the Table 3.8a footnote applies. Where the adjoining site is a grouped dwelling development, give the percentage of each grouped dwelling site area, excluding common property.

### Chapter 4 Part 2 readings

Part 2.0:
- building.side_setback_m (A2.4.1): the least side setback of the building excluding any wall built to the boundary that is assessed as a boundary wall under A2.4.1-r2 and -r3. Otherwise a Table 2.1 boundary wall would always fail the 4 m side setback at R80 to MR1.
- building.boundary_wall_storeys (A2.4.1-r2): 0 where no wall is built to a side boundary.
- building.boundary_wall_length_pct (A2.4.1-r3): each boundary wall's length as a % of the boundary it abuts, the larger where walls are on both sides (note 4 read per boundary; verify).
- building.boundary_walls.adjoining_wall_exists (from the Chapter 2 vocabulary): Table 2.1 note 2, the wall abuts an existing or simultaneously constructed wall of equal or greater proportions.
- building.separation_storeys (A2.7.1, A2.7.1-r1): storeys of the taller of the facing buildings (within site), or of the building facing the boundary (to the adjoining boundary), for the Table 2.7 'up to 4 storeys / 5 storeys and above' band.
- building.height_m (A2.2.1-r1): height above natural ground level in metres, compared with the Table 2.2 metres at the Table 2.1 storey limit.

Part 3.0:
- overshadow.adjoining_pct, adjoining.south.r_code (A3.2.3): the adjoining lot receiving the shadow; percent of its site area at midday 21 June.
- overshadow.solar_collectors_affected (A3.2.4): true where the development reduces direct sun on 21 June below 4 hours for any existing solar collector on an adjoining site coded R40 or less.
- site.significant_tree_retained (A3.3.4 7% concession, A3.3.7 shortfall): read as Table 3.3a 'existing tree(s) retained on site'.
- landscape.deep_soil_pct (A3.3.4, A3.3.7): total deep soil area as % of site area.
- landscape.cos.solar_access_pct (A3.4.3): highest share of any one COS area receiving at least 2 hours of direct sun between 9am and 3pm on 21 June.
- landscape.cos.universally_accessible (A3.4.2): every COS area on the ground floor or a lift-served floor is universally accessible from the primary street entry.
- privacy.bedroom_study_setback_m (now includes open access walkways), privacy.other_habitable_setback_m, privacy.outdoor_active_setback_m: least cone of vision setback from sources on the first four storeys with a floor level more than 0.5 m above NGL; for A3.5.2 (vacant or unknown neighbour) measured to the lot boundary.
- public_domain.ground_floor_level_difference_m (A3.6.5): the greatest level difference (1.2 m limit).
- public_domain.fence_height_m (A3.6.6): average height of the solid portion of street walls and fences.
- parking.access.count (A3.8.1): vehicle openings visible from the street; site.frontage_m is the street frontage.
- site.primary_street_class (A3.8.6): the class of the street the driveway connects to (assumed the primary street).
- parking.behind_street_setback (A3.9.5): outside every street setback.
- parking.resident_spaces_per_dwelling_avg (A3.9.3): as in ch4p1 C2.3.4 (all occupant bays / dwellings). The Table 3.9 minimums use the ch4p1 count facts, not per-dwelling ratios, because per-dwelling ratios cannot express the rounded-up totals.

Part 4.0 (per-dwelling facts describe the least compliant apartment):
- dwellings.with_2h_sun_pct (A4.1.1): a dwelling counts only where both its living rooms and its private open space get 2 hours of direct sun 9am to 3pm on 21 June (Chapter 4 Part 1 counts the primary living space only). dwellings.no_sun_pct is per building; supply the worst building.
- dwellings.min.openings_two_walls (A4.2.1): true when every habitable room has openings on at least two walls.
- dwellings.cross_ventilated_pct (A4.2.2(a)): of dwellings in the first nine storeys only.
- building.height_storeys (A4.2.2(c) condition): the tallest building's storeys; the clause applies to dwellings on the 10th storey and above.
- dwellings.min.bedroom_area_m2, dwellings.min.bedroom_min_dim_m (A4.3.2-r1): the smallest bedroom other than a master bedroom, excluding robes.
- dwellings.min.primary_living_min_dim_m (A4.3.2-r2): read as the living room minimum dimension of Table 4.3b.
- dwellings.min.pos_area_m2, pos_min_dim_m, pos_dwelling_category (A4.4.1, Table 4.4): category ground_floor covers 'ground floor / apartment with a terrace'; 3bed_plus covers the printed '3 bedroom' row. Area excludes service areas and storage (A4.6.3 footnote).
- dwellings.min.storage_* (A4.6.1, Table 4.6 in m2): as Chapter 4 Part 1; storage_bedrooms keys table-4.6.
- dwellings.silver_level_pct (A4.9.1(a)): Silver Level or better (Gold, Platinum count).
- building.storeys (A4.10.2 condition, > 4).
- building.street_setback_m (A4.10.5): read as the primary street setback.
- landscape.plan_provided (A4.12.1): true only if prepared by a competent landscape designer and including a species list and irrigation plan.
- adaptive_reuse.applies (A4.13.1, A4.13.2): the proposal adapts an existing building with new additions.
- proposal.mixed_use (A4.14.3 to A4.14.5).
- landscape.stormwater_retained_on_site (A4.16.2): as in ch4p1 C1.4.1.
- services.waste.plan_provided (A4.17.2): a Level 1 WMP, Design Phase.
- services.waste.communal_storage_area_m2 (A4.17.4 trigger): above 0 where a communal waste storage area is provided.
- Judgment clauses with no fact: A3.5.5 overlooking within the site, A3.9.6 parking screening, A4.18.1 utilities integration; dwellings per core is DG 4.5.3 guidance only.

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

## apartments (Chapter 4 Part 1 only)

Per-dwelling facts describe the least compliant apartment unless the clause is written as a
share of dwellings.

| Fact | Type | Meaning |
|---|---|---|
| dwellings.min.pos_area_m2 | number | smallest private open space (balcony, terrace or courtyard) of any apartment (Table 1.1a) |
| dwellings.min.pos_min_dim_m | number | |
| dwellings.min.pos_dwelling_category | studio_1bed / 2bed / 3bed_plus / ground_floor | Table 1.1a size category of the apartment that dwellings.min.pos_area_m2 and pos_min_dim_m describe; a ground floor dwelling is ground_floor whatever its bedrooms (C1.1.1 to C1.1.1-r3) |
| dwellings.balconies_provided | bool | any apartment has a balcony (C1.1.2 condition) |
| dwellings.min.balcony_unscreened_perimeter_pct | number | lowest % of balcony perimeter unscreened (C1.1.2) |
| dwellings.min.primary_living_min_dim_m | number | smallest primary living space dimension (C2.1.1, 3.8 m) |
| dwellings.max.single_aspect_living_depth_ratio | number | depth of a single-aspect living space divided by ceiling height (C2.1.3, max 3) |
| dwellings.min.bedroom_area_m2 | number | C2.1.4 (9 m2) |
| dwellings.min.bedroom_min_dim_m | number | C2.1.4 (2.7 m) |
| dwellings.min.ceiling_height_habitable_m | number | C2.1.5 (2.65 m) |
| dwellings.min.ceiling_height_non_habitable_m | number | C2.1.5 (2.4 m) |
| dwellings.min.internal_floor_area_m2 | number | smallest apartment against Table 2.1a by bedroom count |
| dwellings.min.bedrooms_of_smallest | int | bedroom count of that apartment |
| dwellings.min.bathrooms_of_smallest | int | bathrooms in the apartment tested for C2.1.6 (Table 2.1a 1-bath / 2-bath rows; +5 m2 per additional bathroom) |
| dwellings.min.separate_toilets_of_smallest | int | additional separate toilets in that apartment (+3 m2 each, Table 2.1a note); 0 where none |
| dwellings.max_same_bedroom_count_pct | number | share of dwellings with the same bedroom count (C2.1.7, 80%) |
| dwellings.min.storage_area_m2 | number | Table 2.1b |
| dwellings.min.storage_min_dim_m | number | |
| dwellings.min.storage_bedrooms | int | bedroom count of the apartment with the least compliant storage; key for Table 2.1b |
| dwellings.min.storage_height_m | number | lowest storage area height (Table 2.1b, 2.1 m) |
| dwellings.storage_behind_street_setback | bool | every apartment's storage is behind the primary street setback (C2.1.8) |
| dwellings.storage_opening_not_inward | bool | every storage area is accessed via an opening that does not open inwards (C2.1.8) |
| dwellings.storage_door_on_greater_dim_80pct_openable | bool | where a storage dimension is under 1.5 m, the door is on the greater dimension and openable for at least 80% of its length (C2.1.9(ii)) |
| dwellings.min.storage_circulation_m | number | adjacent circulation where dimension reduced to 1 m (C2.1.9, 0.9 m) |
| dwellings.ground_floor_openings_to_car_park | bool | C2.1.10 |
| dwellings.min.ground_floor_opening_to_car_park_setback_m | number | least setback of a major opening of a ground-floor apartment facing directly onto car parking or a non-residential component (C2.1.10, 3 m) |
| dwellings.min.noise_source_to_habitable_wall_m | number | C2.1.11 (1 m) |
| dwellings.min.noise_source_to_bedroom_window_m | number | C2.1.11 (3 m) |
| dwellings.with_2h_sun_pct | number | share of dwellings with 2 hours of direct sun (C2.2.2, 70%) |
| dwellings.no_sun_pct | number | share with no direct sun (C2.2.2, max 15%) |
| dwellings.primary_living_direct_access_to_pos | bool | C2.1.2 |
| landscape.cos.area_m2 | number | communal open space area (Table 1.3a) |
| landscape.cos.min_dim_m | number | |
| landscape.cos.separated_from_noise_odour | bool | C1.3.2 |
| landscape.cos.oriented_to_limit_impacts | bool | C1.3.3 |
| landscape.cos.landscaped_and_lit | bool | C1.2.3 |
| landscape.cos.hard_landscape_area_m2 | number | Table 1.3a accessible/hard landscape area (2 m2 per dwelling up to 100 m2), included in the overall COS (C1.3.1-r1) |
| landscape.cos.max_roofed_pct | number | highest share of any one COS area under a covered roof (C1.3.1-r3, 25% of each area) |
| landscape.cos.in_common_property | bool | COS is on common property (C1.3.1(i)) |
| landscape.cos.behind_street_setback | bool | COS is behind the street setback (C1.3.1(i)) |
| landscape.cos.universally_accessible | bool | C1.3.1(ii) |
| landscape.cos.exclusive_to_residential | bool | COS is for the exclusive use of residents; mixed use only (C1.3.1(iii)) |
| parking.resident_spaces | int | resident bays (Table 2.3a minimum) |
| parking.resident_spaces_per_dwelling_avg | number | average bays per dwelling (C2.3.4, max 2) |
| parking.motorcycle_spaces | int | C2.3.3 |
| parking.bicycle_spaces | int | C2.3.7 |
| parking.bicycle_spaces_visitor | int | |
| parking.visitor_bays_signed_common_property | bool | C2.3.6 |
| building.separation_same_lot_m | number | separation between buildings on the same lot (C3.4.6) |
| building.same_lot_separation_applies | bool | the lot holds more than one building, or a building has portions that face each other (C3.4.6 condition) |
| building.separation_same_lot_wall_height_m | number | height of the taller of the facing walls between buildings, or facing portions of a building, on the same lot (C3.4.6, table-3.4a-separation) |
| building.upper_level_overlook_street | bool | upper-level balcony or window overlooks the street (C3.6.1) |
| building.ground_floor_apartments_separate_entry | bool | C3.6.2 |
| parking.path_of_travel_to_entries | bool | C3.7.10 |
| privacy.between_apartments_same_lot_compliant | bool | C3.9.4 |
| subdivision.truncation_area_added_m2 | number | C4.1.2 (max 20 m2) |

## apartments R80 and above (Chapter 4 Part 2 only)

Per-dwelling facts describe the least compliant apartment, as in the Chapter 4 Part 1 apartments section.

### Part 2.0 Primary development parameters (2.1 to 2.8)

| Fact | Type | Meaning |
|---|---|---|
| building.height_storeys | int | storeys above natural ground level (Table 2.1, Table 2.2) |
| building.height_m | number | building height in metres (Table 2.2 relative height) |
| building.boundary_wall_storeys | int | height of walls built to a side boundary, in storeys (Table 2.1) |
| building.boundary_wall_length_pct | number | boundary wall length as % of the boundary (Table 2.1 note 4, two-thirds) |
| building.ground_floor_commercial | bool | commercial use at ground floor (Table 2.1 note 1: nil street setback) |
| building.street_setback_m | number | minimum setback to the primary or secondary street (A2.3.1) |
| building.side_setback_m | number | minimum side setback (A2.4.1) |
| building.rear_setback_m | number | minimum rear setback (A2.4.1) |
| building.plot_ratio | number | gross floor area divided by site area (A2.5.1) |
| building.depth_m | number | building depth (A2.6.1) |
| building.single_aspect_central_corridor | bool | the development comprises single-aspect apartments on each side of a central circulation corridor (A2.6.1 sets the 20 m limit only for this layout) |
| building.separation_within_site_m | number | separation between buildings or wings within the site (Table 2.7) |
| building.separation_to_boundary_m | number | separation to the adjoining property boundary (Table 2.7) |
| building.separation_storeys | int | storey band of the facing walls for Table 2.7 |
| adjoining.r_code | code | R-coding of the adjoining property on the boundary the building faces, absent for uncoded land (Table 2.7: 9 m to R60 or below, 6 m to R80 or above; key of table-2.7-adjoining) |

### Part 3.0 Siting, landscape, privacy, public domain and parking (3.1 to 3.9)

| Fact | Type | Meaning |
|---|---|---|
| site.has_public_realm_frontage | bool | the site has a street or public realm frontage (A3.2.1 applies; A3.2.2 where false) |
| building.faces_public_realm | bool | buildings on the street or public realm frontage are oriented to face it (A3.2.1) |
| overshadow.solar_collectors_affected | bool | A3.2.4 |
| adjoining.solar_collectors_r40_or_lower | bool | an adjoining site coded R40 or less has existing solar collectors (A3.2.4 trigger) |
| landscape.existing_trees.qualifying_present | bool | the site has an existing tree meeting the A3.3.1 criteria (healthy and viable, not a listed weed, and height 4 m and/or trunk 160 mm at 1 m and/or canopy 4 m) |
| landscape.existing_trees.qualifying_all_retained | bool | every such tree is retained (A3.3.1) |
| landscape.existing_trees.removal_arboriculture_report | bool | removal of any such tree is supported by an arboriculture report (A3.3.2) |
| landscape.deep_soil_pct | number | deep soil area as % of site (Table 3.3b) |
| landscape.deep_soil.rootable_soil_zone_provided | bool | where a deep soil area is narrower than the Table 3.3b recommended width, an additional rootable soil zone at least 1 m deep and of the Table 3.3b width adjoins it (A3.3.5-r4 to -r6) |
| landscape.deep_soil_permeable_paving_pct | number | highest share of any deep soil area under permeable paving or decking (A3.3.6, 20%) |
| landscape.planting_on_structure_m2 | number | area of planting on structure (A3.3.7) |
| landscape.cos.solar_access_pct | number | share of communal open space with direct sun (A3.4.3) |
| privacy.storey_band | enum | first_four, fifth_and_above; key of reference table table-3.5 only, no rule reads it |
| privacy.living_room_outlook | bool | A3.5.4 |
| dwellings.ground_floor_fronting_count | int | ground floor dwellings fronting a street or public open space (A3.6.1 trigger) |
| dwellings.ground_floor_fronting_direct_access_pct | number | share of those with direct access from the street or POS via their own terrace, balcony or courtyard (A3.6.1, majority) |
| parking.outside_primary_street_setback | bool | no car parking within the primary street setback (A3.6.2); parking.behind_street_setback is all street setbacks (A3.9.5) |
| public_domain.ground_floor_level_difference_m | number | greatest level difference between ground floor and street level (A3.6.5, 1.2 m) |
| public_domain.ground_floor_level_difference_avg_m | number | average level difference between private terraces, front gardens, ground floor and street level along the frontage (A3.6.5, under 1 m) |
| public_domain.fence_height_m | number | average height of the solid portion of street walls and fences (A3.6.6) |
| services.bins_outside_street_setback_not_visible | bool | bins are outside the primary street setback and not visible from the primary street (A3.6.8) |
| public_domain.entry_from_street | bool | A3.7.x |
| public_domain.entries_weather_protected | bool | every pedestrian entry is protected from the weather (A3.7.2) |
| services.bins_not_at_primary_entry | bool | no bins at the primary pedestrian entry (A3.7.6) |
| parking.driveway.two_way | bool | the driveway is designed for two-way access (A3.8.6) |
| parking.driveway.parking_to_street_m | number | greatest distance from an on-site car parking space to the street along the driveway (A3.8.6 trigger, 15 m) |
| site.corner_sightline_clear_0_75m | bool | walls, fences and structures within 1.5 m of the street corner are no higher than 0.75 m (A3.8.7-r1) |
| parking.bicycle_secure_undercover_path | bool | resident bicycle parking is secure, undercover and reached by a continuous path of travel from the vehicle or cycle entry (A3.9.1-r2) |
| parking.behind_street_setback | bool | car parking is outside every street setback (A3.9.5) |
| parking.visitor_bays_visible_signed_accessible | bool | visitor bays are clearly visible from the driveway, signed 'Visitor Parking' and accessible from the primary entry or entries (A3.9.7) |
| parking.basement.present | bool | the development has basement parking (A3.9.10 trigger) |
| parking.basement.protrusion_m | number | greatest height of the basement above natural ground level (A3.9.10, 1 m) |

### Part 4.0 Designing the building (4.1 to 4.18)

| Fact | Type | Meaning |
|---|---|---|
| dwellings.habitable_rooms_external_window_visible | bool | every habitable room has at least one window in an external wall, visible from all parts of the room (A4.1.2) |
| dwellings.min.habitable_window_glazing_pct | number | lowest glazed area of any habitable room's windows as % of that room's internal floor area (A4.1.2, 10%) |
| dwellings.min.habitable_window_clear_glazing_pct | number | lowest share of that glazing that is clear glazing (A4.1.2, 50%) |
| dwellings.lightwell_skylight_primary_daylight | bool | any habitable room takes its primary daylight from a lightwell or skylight (A4.1.3) |
| dwellings.min.openings_two_walls | bool | every habitable room has openings on at least two walls (A4.2.1) |
| dwellings.min.opening_centre_separation_m | number | least straight-line distance between the centres of the openings on two walls of a habitable room (A4.2.1, 2 m) |
| dwellings.cross_ventilated_pct | number | share of dwellings in the first nine storeys naturally cross-ventilated (A4.2.2, 60%) |
| dwellings.single_aspect_in_cross_ventilated_share | bool | single aspect apartments are counted in the 60% of A4.2.2(a) (condition of A4.2.2(b)) |
| dwellings.single_aspect_openings_45_90_to_cooling_wind | bool | every such apartment's ventilation openings are oriented 45 to 90 degrees to the prevailing cooling wind (A4.2.2(b)) |
| dwellings.max.single_aspect_room_depth_ratio | number | deepest room of those apartments divided by its ceiling height (A4.2.2(b), max 3) |
| dwellings.balconies_10th_storey_high_low_vents | bool | balconies of dwellings on the 10th storey and above have high and low level ventilation openings (A4.2.2(c)) |
| dwellings.cross_through_end_openings_only_present | bool | the proposal has cross-over or cross-through apartments with openings at either end and none on side walls (condition of A4.2.3) |
| dwellings.max.cross_through_depth_m | number | depth of the deepest such apartment (A4.2.3, 20 m) |
| dwellings.lightwell_primary_fresh_air | bool | any habitable room relies on a lightwell as its primary source of fresh air (A4.2.4) |
| dwellings.min.master_bedroom_area_m2 | number | smallest master bedroom, excluding robes (A4.3.2, 10 m2) |
| dwellings.min.master_bedroom_min_dim_m | number | least master bedroom dimension, excluding robes (A4.3.2, 3 m) |
| dwellings.min.living_room_bedrooms | int | bedroom count of the apartment whose living room has the least margin over Table 4.3b (key for table-4.3b; 0 = studio) |
| dwellings.single_aspect_open_plan_present | bool | the proposal has a single aspect open plan living area (condition of A4.3.4) |
| dwellings.max.single_aspect_open_plan_length_m | number | length of the least compliant single aspect open plan living area, measured from the window (A4.3.4) |
| dwellings.single_aspect_open_plan_ceiling_height_m | number | ceiling height of that same living area (A4.3.4) |
| dwellings.single_aspect_kitchen_furthest | bool | in that living area the kitchen is the furthest point from the window (A4.3.4 allowance) |
| dwellings.pos_accessed_from_habitable_room | bool | every dwelling's private open space is accessed directly from a habitable room (A4.4.1) |
| circulation.corridor_width_m | number | A4.5.x |
| dwellings.bedroom_living_openings_onto_circulation | bool | any bedroom window or major opening to a living room opens directly onto circulation or common space (A4.5.5) |
| dwellings.storage_separate_ventilated_weatherproof | bool | every dwelling's storage is for its exclusive use, separate, ventilated and weatherproof (A4.6.1) |
| noise.exceeds_ncc_minimum | bool | dwellings exceed the NCC acoustic minimum, for example by an AAAC rating or equivalent, normally shown by an acoustic report (A4.7.1) |
| dwellings.noise_source_adjacent_habitable_wall | bool | a listed noise source (garage door, driveway, service area, plant room, building services, mechanical equipment, active communal open space, refuse bins or similar) is adjacent to the external wall of a habitable room (A4.7.2) |
| site.local_housing_mix_requirement | bool | a local housing strategy or relevant local planning instrument sets dwelling mix objectives, proportions or targets for the site (A4.8.1(a)/(b) switch) |
| dwellings.mix_per_local_requirement | bool | the dwelling mix accords with those objectives, proportions or targets (A4.8.1(a)) |
| dwellings.silver_level_pct | number | % of dwellings designed to Livable Housing Design Guidelines Silver Level or better (A4.9.1(a)) |
| dwellings.platinum_level_pct | number | % of dwellings designed to Livable Housing Design Guidelines Platinum Level (A4.9.1(b), 5%) |
| facade.entry_awnings_provided | bool | awnings define and give weather protection to the building entries (A4.10.5, first limb) |
| facade.signage_provided | bool | signage is proposed on the building; scopes A4.10.6 |
| roof.useable_space_provided | bool | an accessible, useable roof space (terrace, communal or private open space) is proposed; scopes A4.11.3 |
| landscape.plan_provided | bool | a landscape plan is provided (A4.12.1) |
| `landscape.on_structure.<type>.provided` | bool | plants of this Table 4.12 type are planted on a building structure (podium, terrace, wall, roof); `<type>` is large_tree, medium_tree, small_tree, small_ornamental, shrub, ground_cover, turf (A4.12.3 to A4.12.3-r6) |
| `landscape.on_structure.<type>.min_soil_volume_m3` | number | smallest soil volume given to any planter of that type (trees and small ornamentals) |
| `landscape.on_structure.<type>.min_soil_depth_m` | number | smallest soil depth, in metres, given to any planter of that type (all types) |
| `landscape.on_structure.<type>.min_soil_area_m2` | number | smallest soil area given to any planter of that type (trees and small ornamentals) |
| `landscape.on_structure.<type>.min_soil_dim_m` | number | smallest soil area dimension given to any planter of that type (trees and small ornamentals) |
| landscape.on_structure.plant_type | enum | key of the reference table table-4.12 only; no rule reads it |
| adaptive_reuse.applies | bool | the proposal adapts an existing building with new additions (A4.13.1, A4.13.2) |
| adaptive_reuse.heritage_value | bool | the existing building being adapted has heritage value (local planning framework, Heritage Act 2018 or Commonwealth listing); scopes A4.13.1 |
| site.mixed_use_area_designated | bool | the site is in a mixed use area designated in the local planning framework; scopes A4.14.1 |
| mixed_use.nonres_access_from_street_or_primary_entry | bool | non-residential space is accessed via the street frontage and/or the primary entry (A4.14.3) |
| dwellings.min.nathers_margin_stars | number | smallest margin, in NatHERS stars, by which any dwelling exceeds the NCC per-dwelling (lower) benchmark (A4.15.1(b), footnote 1) |
| energy.significant_initiative | bool | at least one significant energy efficiency initiative exceeding minimum practice is proposed (DG 4.15.1 list or an evidenced alternative) (A4.15.1(a)) |
| water.individual_metering | bool | every dwelling is individually metered for water (A4.16.1) |
| water.overland_flow_path | bool | an overland flow path conveys major rainfall event runoff safely to the local stormwater drainage system (A4.16.3) |
| services.waste.walga_better_practice | bool | waste storage facilities follow the Better Practice considerations of the WALGA Multiple Dwelling Waste Management Plan Guidelines, or local government requirements (A4.17.1) |
| services.waste.plan_provided | bool | a Level 1 waste management plan (Design Phase) is provided (A4.17.2) |
| services.waste.bin_area_per_wmp | bool | bin area holds the number of bins the Level 1 WMP (or local government) requires for separate green waste, recycling and general waste (A4.17.3) |
| services.waste.communal_screened_from_view | bool | communal waste storage is screened from view from the street, open space and private dwellings (A4.17.4) |
| services.fibre_ready | bool | development is fibre-to-premises ready throughout the site and to every dwelling (A4.18.2) |
