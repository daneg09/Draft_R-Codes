# Chapter 4 Part 2 Apartments R80 and above: digest

Version draft-2026-10-24. Applies to multiple_dwelling; coding R80+,LR1,MR1,MR2,HR1,HR2,HR3,R-PA,LR,MR,HR,R-AC0,R-AC1,R-AC2,R-AC3,R-AC4; pathway performance. 169 provisions, 21 flagged ⚑.
Testable column A; a provision not met falls back to the element's O record (DG informs it). Full text: `elements/ch4p2/<element>.md`.

Line, fields split by `;`: `ID` title; kind (m measurable, c conditional, j judgment; /col if not A); coding (= as heading); facts (count and the first two; the full list is under the provision's heading in the pack); test (a table is looked up by coding unless `by` says otherwise); exc n: labels; fb (fallback) if not the element's; ⚑ verify. `site.r_code` is implied by every coding and is not counted.
Find a provision in its pack by grepping for its heading, e.g. ``^### `C3.3.1` ``, and read that section only.

Note: Entirely performance-based (Chapter 1B). Acceptable Outcomes (A) are the testable provisions; an A that is not met is assessed against the element Objectives (O) with Design Guidance (DG) informing …

## 2.1 Primary development parameters (coding all; fb O2.1)
- `T2.1` Table 2.1 Primary Development Parameters …;j/table;=;-;judgment

## 2.2 Building height (coding all; fb O2.2)
- `A2.2.1` Building height in storeys within Table 2.1 …;m;=;building.height_storeys;<= Table 2.1-height-storeys
- `A2.2.1-r1` Building height in metres within Table 2.2 …;m;=;building.height_m;<= Table 2.2-max-height-m ⚑

## 2.3 Street setbacks (coding all; fb O2.3)
- `A2.3.1` Primary and secondary street setback at …;m;=;building.{street_setback_m,ground_floor_commercial};>= Table 2.1-street-setback;exc 1: Table 2.1 note 1

## 2.4 Side and rear setbacks (coding all; fb O2.4)
- `A2.4.1` Side setback at least Table 2.1 minimum;m;=;building.side_setback_m;>= Table 2.1-side-setback ⚑
- `A2.4.1-r1` Rear setback at least Table 2.1 minimum;m;=;building.rear_setback_m;>= Table 2.1-rear-setback
- `A2.4.1-r2` Boundary wall height (storeys) within Table …;m;=;building.boundary_wall_storeys, building.boundary_walls.adjoining_wall_exists;<= Table 2.1-boundary-wall-storeys;exc 1: Table 2.1 note 2
- `A2.4.1-r3` Boundary wall length no more than two-thirds …;m;R80+;building.boundary_wall_length_pct, building.boundary_walls.adjoining_wall_exists;<= 66.67%;exc 1: Table 2.1 note 2 ⚑
- `A2.4.1-r4` Boundary wall between differently coded …;j;=;-;judgment ⚑
- `A2.4.2` Setback from boundary to achieve 2.7, 3.3 …;j;=;-;judgment

## 2.5 Plot ratio (coding all; fb O2.5)
- `A2.5.1` Plot ratio within Table 2.1 maximum;m;=;building.plot_ratio;<= Table 2.1-plot-ratio

## 2.6 Building depth (coding all; fb O2.6)
- `A2.6.1` Building depth no more than 20 m where …;m;=;building.{depth_m,single_aspect_central_corridor};<= 20 m
- `A2.6.1-r1` Other building depths assessed on merit …;j;=;-;judgment

## 2.7 Building separation (coding all; fb O2.7)
- `A2.7.1` Building separation within site at least …;m;=;3 facts: building.{separation_within_site_m,separation_storeys};>= Table 2.7 by separation_storeys ⚑
- `A2.7.1-r1` Building separation to adjoining property …;m;MR2,HR1,HR2,HR3,HR;3 facts: building.{separation_to_boundary_m,separation_storeys};>= Table 2.7-adjoining by … ⚑

## 2.8 Development incentives for community benefit (coding all; fb O2.8)
- `A2.8` Development incentives for community benefit;j;=;-;judgment

## 3.1 Site analysis and design response (no A provisions; O3.1, DG3.1)

## 3.2 Orientation (coding all; fb O3.2)
- `A3.2.1` Buildings on street or public realm …;c;=;3 facts: building.faces_public_realm, public_domain.entry_from_street;all(yes; yes)
- `A3.2.2` Buildings without street or public realm …;j;=;site.has_public_realm_frontage;judgment
- `A3.2.3` Overshadowing of adjoining property at …;m;=;overshadow.adjoining_pct, site.climate_zone;<= Table 3.2-overshadow by coding
- `A3.2.3-r1` Proportional overshadowing limit where …;c;=;3 facts: adjoining.north_shared_boundary_count, overshadow.proportional_to_shared_boundary;yes ⚑
- `A3.2.4` Existing solar collectors on adjoining sites …;c;=;adjoining.solar_collectors_r40_or_lower, overshadow.solar_collectors_affected;no

## 3.3 Tree canopy and deep soil areas (coding all; fb O3.3)
- `A3.3.1` Existing trees meeting retention criteria …;c;=;3 facts: landscape.existing_trees.{qualifying_all_retained,qualifying_present};yes;exc 1: removal of … ⚑
- `A3.3.2` Removal of tree meeting A3.3.1 criteria is …;c;=;3 facts: landscape.existing_trees.{qualifying_all_retained,qualifying_present};yes
- `A3.3.3` No detrimental impact on, and minimal canopy …;j;=;-;judgment
- `A3.3.4` Deep soil area at least 10% of site area …;m;=;landscape.deep_soil_pct, site.significant_tree_retained;>= 10%;exc 1: existing tree
- `A3.3.4-r1` Deep soil areas co-located with retained or …;j;=;-;judgment
- `A3.3.5-r1` Trees on site under 700 m2: at least 1 …;m;=;landscape.trees.medium_count, site.area_m2;>= 1
- `A3.3.5-r2` Trees on 700-1,000 m2 site: 2 medium trees …;m;=;3 facts: landscape.trees.{large_count,medium_count};any(>= 2; >= 1)
- `A3.3.5-r3` Trees on site over 1,000 m2: 1 large plus 1 …;m;=;3 facts: landscape.trees.{large_count,medium_count};any of 2 tests ⚑
- `A3.3.5-r4` Deep soil per small tree: 9 m2, width 2 m …;m;=;4 facts: landscape.deep_soil.{rootable_soil_zone_provided,small_min_dim_m};all(>= 9 m²; >= 2 m);exc 1: rootable soil zone …
- `A3.3.5-r5` Deep soil per medium tree: 36 m2, width 3 m …;m;=;4 facts: landscape.deep_soil.{medium_min_dim_m,medium_min_m2};all(>= 36 m²; >= 3 m);exc 1: rootable soil zone …
- `A3.3.5-r6` Deep soil per large tree: 64 m2, width 6 m …;m;=;4 facts: landscape.deep_soil.{large_min_dim_m,large_min_m2};all(>= 64 m²; >= 6 m);exc 1: rootable soil zone …
- `A3.3.6` Permeable paving or decking within deep soil …;m;=;landscape.deep_soil_permeable_paving_pct;<= 20%
- `A3.3.7` Deep soil shortfall offset by planting on …;m;=;4 facts: landscape.{deep_soil_pct,planting_on_structure_m2};landscape.planting_on_structure_m2 …

## 3.4 Communal open space (coding all; fb O3.4)
- `A3.4.1` Communal open space: 6 m2 per dwelling up to …;m;=;landscape.cos.area_m2, proposal.dwelling_count;landscape.cos.area_m2 >= min(6 * …
- `A3.4.1-r1` Accessible / hard landscape communal open …;m;=;landscape.cos.hard_landscape_area_m2, proposal.dwelling_count;landscape.cos.hard_landscape_area_m2 …
- `A3.4.1-r2` Communal open space minimum dimension 4 m;m;=;landscape.cos.min_dim_m, proposal.dwelling_count;>= 4 m
- `A3.4.1-r3` Up to 10 dwellings: informal seating …;j;=;proposal.dwelling_count;judgment
- `A3.4.2` Communal open space on ground floor or …;c;=;landscape.cos.{area_m2,universally_accessible};yes
- `A3.4.3` At least one communal open space area 50% …;m;=;landscape.cos.{area_m2,solar_access_pct};>= 50% ⚑
- `A3.4.4` Communal open space co-located with deep …;j;=;landscape.cos.area_m2;judgment
- `A3.4.5` Communal open space separated or screened …;c;=;landscape.cos.{area_m2,separated_from_noise_odour};yes
- `A3.4.6` Communal open space well-lit, minimises …;j;=;landscape.cos.area_m2;judgment
- `A3.4.7` Communal open space designed and oriented to …;j;=;landscape.cos.area_m2;judgment

## 3.5 Visual privacy (coding all; fb O3.5)
- `A3.5.1-r1` Cone of vision setback from bedroom, study …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m;exc 1: cone of vision …
- `A3.5.1-r2` Cone of vision setback from other habitable …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 4.5 m;exc 1: cone of vision …
- `A3.5.1-r3` Cone of vision setback from unenclosed …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 6.0 m;exc 1: cone of vision …
- `A3.5.1-r4` Privacy setback from 5th storey and above …;j;=;adjoining.vacant_or_unknown, privacy.sources_above_0_5m;judgment
- `A3.5.2-r1` Vacant or unknown adjoining site: cone of vision from bedroom, study …;m;=;3 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m
- `A3.5.2-r2` Vacant or unknown adjoining site: cone of vision from other …;m;=;3 facts: adjoining.vacant_or_unknown, privacy.other_habitable_setback_m;>= 4.5 m
- `A3.5.2-r3` Vacant or unknown adjoining site: cone of vision from unenclosed …;m;=;3 facts: adjoining.vacant_or_unknown, privacy.outdoor_active_setback_m;>= 6.0 m
- `A3.5.3` Balconies unscreened for at least 25% of …;m;=;dwellings.balconies_provided, dwellings.min.balcony_unscreened_perimeter_pct;>= 25%
- `A3.5.4` Living rooms have external outlook from at …;c;=;privacy.living_room_outlook;yes
- `A3.5.5` Windows and balconies restrict direct …;j;=;-;judgment

## 3.6 Public domain interface (coding all; fb O3.6)
- `A3.6.1` Majority of ground floor dwellings fronting …;m;=;dwellings.{ground_floor_fronting_count,ground_floor_fronting_direct_access_pct};> 50%
- `A3.6.2` Car parking not located within primary …;c;=;parking.outside_primary_street_setback;yes
- `A3.6.2-r1` Ground-level car parking behind street …;j;=;-;judgment
- `A3.6.3` Upper level balconies and/or windows …;c;=;building.{storeys,upper_level_overlook_street};yes
- `A3.6.4` Balustrading mixes visually opaque and …;j;=;-;judgment
- `A3.6.5` Level change between terraces, front …;m;=;public_domain.{ground_floor_level_difference_avg_m,ground_floor_level_difference_m};all(< 1.0 m; <= 1.2 m)
- `A3.6.6` Front fencing visually permeable above 1.2 …;m;=;3 facts: building.front_fence.{permeable_above_m,present};all(<= 1.2 m; <= 1.2 m)
- `A3.6.7` Frontage fencing, landscaping and other …;j;=;-;judgment
- `A3.6.8` Bins not in primary street setback or …;c;=;services.bins_outside_street_setback_not_visible;yes
- `A3.6.9` Services and utilities in primary street …;j;=;-;judgment

## 3.7 Pedestrian access and entries (coding all; fb O3.7)
- `A3.7.1` Pedestrian entries connected by legible …;c;=;parking.path_of_travel_to_entries;yes
- `A3.7.2` Pedestrian entries protected from weather;c;=;public_domain.entries_weather_protected;yes
- `A3.7.3` Pedestrian entries well-lit, visible from …;j;=;-;judgment
- `A3.7.4` Shared zone pedestrian path clearly …;j;=;-;judgment
- `A3.7.5` Services and utilities at pedestrian entry …;j;=;-;judgment
- `A3.7.6` Bins not located at primary pedestrian entry;c;=;services.bins_not_at_primary_entry;yes

## 3.8 Vehicle access (coding all; fb O3.8)
- `A3.8.1` One vehicle opening visible from street per …;m;=;parking.access.count, site.frontage_m;parking.access.count <= max(1 … ⚑
- `A3.8.2` Vehicle entries identifiable from street …;j;=;-;judgment
- `A3.8.3` Vehicle entries adequately separated from …;j;=;-;judgment
- `A3.8.4` Vehicle circulation avoids headlights …;j;=;-;judgment
- `A3.8.5` Driveway width kept to functional minimum;j;=;-;judgment
- `A3.8.6` Two-way driveway where it serves more than …;c;=;4 facts: parking.driveway.{dwellings_served,parking_to_street_m};yes ⚑
- `A3.8.7` Walls, fences and structures no higher than 0.75 m within 1.5 m of …;c;=;parking.sightlines.clear_0_75m_within_1_5m;yes
- `A3.8.7-r1` Walls, fences and structures no higher than 0.75 m within 1.5 m …;c;=;site.{corner_lot,corner_sightline_clear_0_75m};yes ⚑

## 3.9 Car and bicycle parking (coding all; fb O3.9)
- `A3.9.1` Resident bicycle parking: 0.5 spaces per …;m;=;parking.bicycle_spaces, proposal.dwelling_count;parking.bicycle_spaces >= round(0.5 …
- `A3.9.1-r1` Visitor bicycle parking: 0.1 spaces per …;m;=;parking.bicycle_spaces_visitor, proposal.dwelling_count;parking.bicycle_spaces_visitor >= …
- `A3.9.1-r2` Bicycle parking secure, undercover and …;c;=;parking.{bicycle_secure_undercover_path,bicycle_spaces};yes ⚑
- `A3.9.2` Resident car parking: no minimum in Location …;m;=;parking.resident_spaces;>= Table 3.9-resident by location
- `A3.9.2-r1` Visitor car parking, 5 or more dwellings …;m;=;3 facts: parking.visitor_spaces, proposal.dwelling_count;parking.visitor_spaces >= Table …
- `A3.9.2-r2` Motorcycle/scooter parking, more than 20 …;m;=;parking.motorcycle_spaces, proposal.dwelling_count;parking.motorcycle_spaces >= … ⚑
- `A3.9.3` Maximum car parking: 2 bays per dwelling …;m;=;parking.resident_spaces_per_dwelling_avg;<= 2 ⚑
- `A3.9.4` Car parking and vehicle circulation designed …;c;=;parking.as2890_compliant;yes
- `A3.9.5` Car parking areas not located within street …;c;=;parking.behind_street_setback;yes
- `A3.9.5-r1` Car parking areas not visually prominent …;j;=;-;judgment
- `A3.9.6` Car parking designed, landscaped or screened …;j;=;-;judgment
- `A3.9.7` Visitor parking visible from driveway …;c;=;parking.{visitor_bays_visible_signed_accessible,visitor_spaces};yes
- `A3.9.8` Parking shade structures integrate with …;j;=;-;judgment
- `A3.9.9` Uncovered at-grade parking planted with at …;m;=;landscape.parking_shade_trees, parking.uncovered_at_grade_spaces;4 * landscape.parking_shade_trees >= …
- `A3.9.10` Basement parking protrudes no more than 1 m …;m;=;parking.basement.{present,protrusion_m};<= 1.0 m ⚑
- `A3.9.10-r1` Protruding basement designed or screened to …;j;=;parking.basement.present;judgment

## 4.1 Solar and daylight access (coding all; fb O4.1)
- `A4.1.1` Climate zones 4 to 6: at least 70% of …;m;=;3 facts: site.climate_zone, dwellings.with_2h_sun_pct;all(>= 70%; <= 15%)
- `A4.1.2` Every habitable room has external-wall …;m;=;3 facts: dwellings.habitable_rooms_external_window_visible, dwellings.min.habitable_window_glazing_pct;all(yes; >= 10%; >= 50%)
- `A4.1.3` Lightwells and skylights are not primary …;c;=;dwellings.lightwell_skylight_primary_daylight;no
- `A4.1.4` Orientation and external shading limit …;j;=;-;judgment

## 4.2 Natural ventilation (coding all; fb O4.2)
- `A4.2.1` Habitable rooms have openings on at least …;m;=;dwellings.min.{openings_two_walls,opening_centre_separation_m};all(yes; >= 2.0 m) ⚑
- `A4.2.2(a)` At least 60% of dwellings in first nine …;m;=;dwellings.cross_ventilated_pct;>= 60%
- `A4.2.2(b)` Single aspect apartments counted in 60% …;m;=;3 facts: dwellings.{single_aspect_in_cross_ventilated_share,single_aspect_openings_45_90_to_cooling_wind};all(yes; <= 3)
- `A4.2.2(c)` Dwellings at 10th storey or above: balconies …;c;=;building.height_storeys, dwellings.balconies_10th_storey_high_low_vents;yes
- `A4.2.3` Cross-over and cross-through apartments with …;m;=;dwellings.cross_through_end_openings_only_present, dwellings.max.cross_through_depth_m;<= 20 m
- `A4.2.4` No habitable room relies on lightwell as its …;c;=;dwellings.lightwell_primary_fresh_air;no

## 4.3 Size and layout of dwellings (coding all; fb O4.3)
- `A4.3.1` Minimum internal floor area per Table 4.3a …;m;=;4 facts: dwellings.min.{internal_floor_area_m2,bedrooms_of_smallest};dwellings.min.internal_floor_area_m2 … ⚑
- `A4.3.2` Master bedroom at least 10 m2 and 3 m …;m;=;dwellings.min.{master_bedroom_area_m2,master_bedroom_min_dim_m};all(>= 10 m²; >= 3 m)
- `A4.3.2-r1` Other bedrooms at least 9 m2 and 3 m minimum …;m;=;dwellings.min.{bedroom_area_m2,bedroom_min_dim_m};all(>= 9 m²; >= 3 m)
- `A4.3.2-r2` Living room minimum dimension 3.6 m …;m;=;dwellings.min.{primary_living_min_dim_m,living_room_bedrooms};>= Table 4.3b by …
- `A4.3.3` Ceiling heights at least 2.7 m to habitable …;m;=;dwellings.min.{ceiling_height_habitable_m,ceiling_height_non_habitable_m};all(>= 2.7 m; >= 2.4 m)
- `A4.3.4` Single aspect open plan living area no …;m;=;4 facts: dwellings.single_aspect_open_plan_present, dwellings.max.single_aspect_open_plan_length_m;dwellings.max.single_aspect_open_plan …;exc 1: kitchen at the …

## 4.4 Private open space and balconies (coding all; fb O4.4)
- `A4.4.1` Each dwelling has private open space …;m;=;4 facts: dwellings.min.{pos_area_m2,pos_min_dim_m};all of 3 tests
- `A4.4.2` Privacy screening does not screen whole open …;j;=;-;judgment
- `A4.4.3` Private open space detailing, materials and …;j;=;-;judgment
- `A4.4.4` Services and fixtures in private open space …;j;=;-;judgment

## 4.5 Circulation and common spaces (coding all; fb O4.5)
- `A4.5.1` Circulation corridors at least 1.5 m wide;m;=;circulation.corridor_width_m;>= 1.5 m
- `A4.5.2` Circulation and common spaces designed for …;j;=;-;judgment
- `A4.5.3` Circulation and common spaces allow passive …;j;=;-;judgment
- `A4.5.4` Circulation and common spaces lit at night …;j;=;-;judgment
- `A4.5.5` Bedroom windows and major openings to living …;c;=;dwellings.bedroom_living_openings_onto_circulation;no
- `A4.5.5-r1` Dwelling openings near circulation spaces …;j;=;-;judgment

## 4.6 Storage (coding all; fb O4.6)
- `A4.6.1` Each dwelling has exclusive separate …;m;=;5 facts: dwellings.min.{storage_area_m2,storage_bedrooms};all of 4 tests
- `A4.6.2` Stores not directly accessible from dwelling …;j;=;-;judgment
- `A4.6.3` Separate or open-space storage is integrated …;j;=;-;judgment

## 4.7 Managing the impact of noise (coding all; fb O4.7)
- `A4.7.1` Dwellings exceed NCC acoustic minimums;c;=;noise.exceeds_ncc_minimum;yes
- `A4.7.2` Noise sources not adjacent to habitable room …;m;=;dwellings.noise_source_adjacent_habitable_wall, dwellings.min.noise_source_to_bedroom_window_m;all(no; >= 3.0 m)
- `A4.7.3` Major openings to habitable rooms oriented …;j;=;-;judgment

## 4.8 Dwelling mix (coding all; fb O4.8)
- `A4.8.1(a)` Where local housing strategy or local …;c;=;site.local_housing_mix_requirement, dwellings.mix_per_local_requirement;yes ⚑
- `A4.8.1(b)` No local housing strategy and more than 10 …;m;=;3 facts: site.local_housing_mix_requirement, proposal.dwelling_count;<= 80% ⚑
- `A4.8.2` Dwelling types well distributed, with mix on …;j;=;-;judgment

## 4.9 Universal design (coding all; fb O4.9)
- `A4.9.1` 20% of dwellings at Silver Level, or 5% at …;m;=;dwellings.{silver_level_pct,platinum_level_pct};any(>= 20%; >= 5%)

## 4.10 Facade design (coding all; fb O4.10)
- `A4.10.1` Façade scale, articulation, materiality and …;j;=;-;judgment
- `A4.10.2` Buildings over four storeys have defined …;j;=;building.storeys;judgment
- `A4.10.3` Façade elements relate to key datum lines of …;j;=;-;judgment
- `A4.10.4` Building services fixtures integrated in …;j;=;-;judgment
- `A4.10.5` Street setback of 1 m or less: awnings …;c;=;building.street_setback_m, facade.entry_awnings_provided;yes
- `A4.10.5-r1` Entry awnings integrated into façade and …;j;=;building.street_setback_m;judgment
- `A4.10.6` Signage, where provided, integrated and …;j;=;facade.signage_provided;judgment

## 4.11 Roof design (coding all; fb O4.11)
- `A4.11.1` Roof form or top of building complements …;j;=;-;judgment
- `A4.11.2` Roof-top building services not visually …;j;=;-;judgment
- `A4.11.3` Useable roof space is safe and limits …;j;=;roof.useable_space_provided;judgment

## 4.12 Landscape design (coding all; fb O4.12)
- `A4.12.1` Landscape plan by competent landscape …;c;=;landscape.plan_provided;yes
- `A4.12.2` Landscaped areas support mature shade trees …;j;=;-;judgment
- `A4.12.3` Planting on structure, large tree …;m;=;5 facts: landscape.on_structure.large_tree.{provided,min_soil_volume_m3};all(>= 76.8 m³; >= 1.2 m; >= 64 m² …
- `A4.12.3-r1` Planting on structure, medium tree …;m;=;5 facts: landscape.on_structure.medium_tree.{provided,min_soil_volume_m3};all(>= 36 m³; >= 1.0 m; >= 36 m²; >= …
- `A4.12.3-r2` Planting on structure, small tree …;m;=;5 facts: landscape.on_structure.small_tree.{provided,min_soil_volume_m3};all(>= 7.2 m³; >= 0.8 m; >= 9 m²; >= …
- `A4.12.3-r3` Planting on structure, small ornamentals …;m;=;5 facts: landscape.on_structure.small_ornamental.{provided,min_soil_volume_m3};all(>= 3.2 m³; >= 0.8 m; >= 4 m²; >= …
- `A4.12.3-r4` Planting on structure, shrubs: soil depth …;m;=;landscape.on_structure.shrub.{provided,min_soil_depth_m};>= 0.5 m
- `A4.12.3-r5` Planting on structure, ground cover: soil …;m;=;landscape.on_structure.ground_cover.{provided,min_soil_depth_m};>= 0.3 m
- `A4.12.3-r6` Planting on structure, turf: soil depth 200 …;m;=;landscape.on_structure.turf.{provided,min_soil_depth_m};>= 0.2 m
- `A4.12.4` Building services fixtures integrated in …;j;=;-;judgment

## 4.13 Adaptive reuse (coding all; fb O4.13)
- `A4.13.1` Additions to heritage buildings do not mimic …;j;=;adaptive_reuse.{applies,heritage_value};judgment
- `A4.13.2` New additions reference and interpret scale …;j;=;adaptive_reuse.applies;judgment

## 4.14 Mixed use (coding all; fb O4.14)
- `A4.14.1` Designated mixed use area: ground floor …;j;=;site.mixed_use_area_designated;judgment
- `A4.14.2` Ground floor uses, including non-commercial …;j;=;-;judgment
- `A4.14.3` Non-residential space accessed via street …;c;=;proposal.mixed_use, mixed_use.nonres_access_from_street_or_primary_entry;yes
- `A4.14.4` Non-residential tenancies have parking …;j;=;proposal.mixed_use;judgment
- `A4.14.5` Mixed use designed to mitigate …;j;=;proposal.mixed_use;judgment

## 4.15 Energy efficiency (coding all; fb O4.15)
- `A4.15.1` One significant energy initiative beyond …;m;=;dwellings.min.nathers_margin_stars, energy.significant_initiative;any(>= 0.5; yes)

## 4.16 Water management and conservation (coding all; fb O4.16)
- `A4.16.1` Dwellings individually metered for water;c;=;water.individual_metering;yes
- `A4.16.2` Stormwater runoff from small rainfall events …;c;=;landscape.stormwater_retained_on_site;yes
- `A4.16.3` Overland flow path conveys major rainfall …;c;=;water.overland_flow_path;yes

## 4.17 Waste management (coding all; fb O4.17)
- `A4.17.1` Waste storage facilities per WALGA Better …;c;=;services.waste.walga_better_practice;yes
- `A4.17.2` Level 1 Waste Management Plan (Design Phase) …;c;=;services.waste.plan_provided;yes
- `A4.17.3` Bin area sized for separate green waste …;c;=;services.waste.bin_area_per_wmp;yes
- `A4.17.4` Communal waste storage screened from view …;c;=;services.waste.{communal_storage_area_m2,communal_screened_from_view};yes

## 4.18 Utilities (coding all; fb O4.18)
- `A4.18.1` Utilities in front setback, at entry or on …;j;=;-;judgment
- `A4.18.2` Fibre-to-premises ready throughout site and …;c;=;services.fibre_ready;yes
- `A4.18.3` Hot water, AC condensers and clotheslines …;j;=;-;judgment
- `A4.18.4` Laundries convenient, secure …;j;=;-;judgment
