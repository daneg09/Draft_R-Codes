# Chapter 4 Part 1 Apartments R10 to R60: digest

Version draft-2026-10-24. Applies to multiple_dwelling; coding R10-R60; pathway deemed-exempt-or-merit. 164 provisions, 32 flagged ⚑.
Testable column C; a provision not met falls back to the element's M record. Full text: `elements/ch4p1/<element>.md`.

Line, fields split by `;`: `ID` title; kind (m measurable, c conditional, j judgment; /col if not C); coding (= as heading); facts (count and the first two; the full list is under the provision's heading in the pack); test (a table is looked up by coding unless `by` says otherwise); exc n: labels; fb (fallback) if not the element's; ⚑ verify. `site.r_code` is implied by every coding and is not counted.
Find a provision in its pack by grepping for its heading, e.g. ``^### `C3.3.1` ``, and read that section only.

Note: Apartments (multiple dwellings) in areas coded R10 to R60. Content twin of Chapter 3 for most of Parts 1, 3 and 4, but element numbering differs: 1.3 is communal open space and water is 1.4; there is …

## 1.1 Private open space (coding R10-R25; fb M1.1)
- `C1.1.1` Private open space per apartment: minimum area (Table 1.1a), R30 to …;m;R30-R60;dwellings.min.{pos_area_m2,pos_dwelling_category};>= Table 1.1a by …
- `C1.1.1-r1` Private open space per apartment: minimum dimension (Table 1.1a) …, R30-R60;m;R30-R60;dwellings.min.{pos_min_dim_m,pos_dwelling_category};>= Table 1.1a-dim by …
- `C1.1.1-r2` Private open space per apartment: minimum area (Table 1.1a), R10 to …;m;=;dwellings.min.{pos_area_m2,pos_dwelling_category};>= Table 1.1a by …
- `C1.1.1-r3` Private open space per apartment: minimum dimension (Table 1.1a) …, R10-R25;m;=;dwellings.min.{pos_min_dim_m,pos_dwelling_category};>= Table 1.1a-dim by …
- `C1.1.2` Balconies unscreened for at least 25% of …;m;all;dwellings.balconies_provided, dwellings.min.balcony_unscreened_perimeter_pct;>= 25%

## 1.2 Trees and landscaping (coding all; fb M1.2)
- `C1.2.1` Soft landscaping minimum 15% of site;m;=;3 facts: landscape.soft_area_m2, site.area_m2;>= 15% of site.area_m2;exc 1: C1.2.6
- `C1.2.1-r1` Soft landscaping minimum dimension 1 m;m;=;landscape.soft_min_dim_m;>= 1 m
- `C1.2.2` Primary street setback area minimum 30% soft …;m;=;landscape.{street_setback_soft_area_m2,street_setback_area_m2};>= 30% of …
- `C1.2.3` Communal street landscaped and lit;c;=;site.{has_communal_street,communal_street_landscaped_and_lit};yes
- `C1.2.3-r1` Communal open space landscaped and lit;c;=;landscape.cos.{area_m2,landscaped_and_lit};yes
- `C1.2.4` Minimum trees on lot under 700 m2: 1 medium …;m;=;4 facts: site.area_m2, landscape.trees.small_count;all(>= 1; >= 2) ⚑
- `C1.2.4-r1` Minimum trees on lot of 700 to 1,000 m2: 2 …;m;=;4 facts: site.area_m2, landscape.trees.small_count;any(>= 2; all(>= 1; >= 1)) ⚑
- `C1.2.4-r2` Minimum trees on lot over 1,000 m2: as 700 …;m;=;4 facts: site.area_m2, landscape.trees.small_count;any of 2 tests ⚑
- `C1.2.4-r3` Deep soil area per small tree: 9 m2, minimum …;m;=;3 facts: landscape.trees.small_count, landscape.deep_soil.small_min_m2;all(>= 9 m²; >= 1.5 m)
- `C1.2.4-r4` Deep soil area per medium tree: 36 m2 …;m;=;3 facts: landscape.trees.medium_count, landscape.deep_soil.medium_min_m2;all(>= 36 m²; >= 3 m)
- `C1.2.4-r5` Deep soil area per large tree: 64 m2 …;m;=;3 facts: landscape.trees.large_count, landscape.deep_soil.large_min_m2;all(>= 64 m²; >= 6 m)
- `C1.2.5` Shade trees for uncovered at-grade car …;m;=;parking.uncovered_at_grade_spaces, landscape.parking_shade_trees;4 * landscape.parking_shade_trees >= …
- `C1.2.7` Tree protection zone for retained …;c;=;site.{significant_tree_retained,retained_tree_root_zone_provided};yes
- `C1.2.8` Landscaping plan for apartments;c;=;landscape.landscaping_plan_provided;yes

## 1.3 Communal open space (coding all; fb M1.3)
- `C1.3.1` Communal open space: 6 m2 per dwelling up to …;m;=;proposal.dwelling_count, landscape.cos.area_m2;landscape.cos.area_m2 >= min(6 * …
- `C1.3.1(i)` Communal open space in common property and …;c;=;3 facts: proposal.dwelling_count, landscape.cos.in_common_property;all(yes; yes)
- `C1.3.1(ii)` Communal open space universally accessible …;c;=;proposal.dwelling_count, landscape.cos.universally_accessible;yes
- `C1.3.1(iii)` Communal open space exclusive to residential …;c;=;3 facts: proposal.{dwelling_count,mixed_use};yes
- `C1.3.1-r1` Communal open space: accessible hard …;m;=;proposal.dwelling_count, landscape.cos.hard_landscape_area_m2;landscape.cos.hard_landscape_area_m2 …
- `C1.3.1-r2` Communal open space minimum dimension 4 m;m;=;proposal.dwelling_count, landscape.cos.min_dim_m;>= 4 m
- `C1.3.1-r3` Communal open space: maximum covered roof …;m;=;proposal.dwelling_count, landscape.cos.max_roofed_pct;<= 25%
- `C1.3.2` Communal open space separated or screened …;c;=;landscape.cos.{area_m2,separated_from_noise_odour};yes
- `C1.3.3` Communal open space designed and oriented to …;c;=;landscape.cos.{area_m2,oriented_to_limit_impacts};yes

## 1.4 Water management and conservation (coding all; fb M1.4)
- `C1.4.1` Stormwater from small rainfall event …;c;=;landscape.{stormwater_retained_on_site,stormwater_to_system_required};yes;exc 1: C1.4.2

## 2.1 Size and layout of dwellings (coding R30-R60; fb M2.1)
- `C2.1.1` Primary living space can accommodate 3.8 m x …;m;=;dwellings.min.primary_living_min_dim_m;>= 3.8 m
- `C2.1.2` Primary living space has direct physical and …;c;=;dwellings.primary_living_direct_access_to_pos;yes ⚑
- `C2.1.3` Single-aspect primary living space depth at …;m;=;dwellings.max.single_aspect_living_depth_ratio;<= 3
- `C2.1.4` Bedrooms at least 9 m2 and 2.7 m x 2.7 m;m;=;dwellings.min.{bedroom_area_m2,bedroom_min_dim_m};all(>= 9.0 m²; >= 2.7 m)
- `C2.1.5` Ceiling heights at least 2.65 m (habitable) …;m;=;dwellings.min.{ceiling_height_habitable_m,ceiling_height_non_habitable_m};all(>= 2.65 m; >= 2.4 m)
- `C2.1.6` Minimum internal floor area per Table 2.1a …;m;=;4 facts: dwellings.min.{internal_floor_area_m2,bedrooms_of_smallest};dwellings.min.internal_floor_area_m2 … ⚑
- `C2.1.7` More than 10 apartments: no more than 80% …;m;=;proposal.dwelling_count, dwellings.max_same_bedroom_count_pct;<= 80%
- `C2.1.8` Dedicated weatherproof storage per Table …;m;all;8 facts: dwellings.min.{storage_area_m2,storage_bedrooms};all of 5 tests;exc 1: C2.1.9
- `C2.1.10` Major openings of ground-floor apartments …;m;=;dwellings.ground_floor_openings_to_car_park, dwellings.min.ground_floor_opening_to_car_park_setback_m;>= 3.0 m
- `C2.1.11` Noise sources at least 1 m from habitable …;m;=;dwellings.min.{noise_source_to_habitable_wall_m,noise_source_to_bedroom_window_m};all(>= 1.0 m; >= 3.0 m)

## 2.2 Solar access and natural ventilation (coding R30-R60; fb M2.2)
- `C2.2.1` Courtyard that is only daylight source to …;m;=;3 facts: building.{courtyard_daylight_only,courtyard_open_to_sky};all(yes; >= 4.0 m²)
- `C2.2.2` Climate zones 4 to 6: at least 70% of …;m;=;3 facts: site.climate_zone, dwellings.with_2h_sun_pct;all(>= 70%; <= 15%)

## 2.3 Parking (coding all; fb M2.3)
- `C2.3.1` Resident car parking per Table 2.3a;m;=;parking.resident_spaces, site.location;>= Table 2.3a by location
- `C2.3.1-r1` Parking: no regional table in Chapter 4 Part …, regional;j;=;site.region;judgment ⚑
- `C2.3.2` Car spaces and manoeuvring areas per …;c;=;parking.as2890_compliant;yes
- `C2.3.3` More than 20 apartments: 0.1 …;m;=;proposal.dwelling_count, parking.motorcycle_spaces;parking.motorcycle_spaces >= … ⚑
- `C2.3.4` R50 and above: occupant parking averages at …;m;R50-R60;parking.resident_spaces_per_dwelling_avg;<= 2
- `C2.3.5` Visitor car parking: 0.1 bays per dwelling …;m;=;3 facts: proposal.dwelling_count, site.location;parking.visitor_spaces >= Table …
- `C2.3.6` Visitor bays marked and signposted, on …;c;=;parking.{visitor_spaces,visitor_bays_signed_common_property};yes
- `C2.3.7` Resident bicycle parking: 0.5 spaces per …;m;=;proposal.dwelling_count, parking.bicycle_spaces;parking.bicycle_spaces >= round(0.5 … ⚑
- `C2.3.7-r1` Visitor bicycle parking: 0.1 spaces per …;m;=;proposal.dwelling_count, parking.bicycle_spaces_visitor;parking.bicycle_spaces_visitor >= … ⚑

## 2.4 Waste management (coding all; fb M2.4)
- `C2.4.1` Dedicated, accessible space for dwelling's …;c;=;services.waste.bin_space_per_lg_requirements;yes
- `C2.4.2` Waste storage bins screened from view;c;=;services.bins_screened;yes
- `C2.4.3` Communal waste storage area separated or …;c;=;services.waste.{communal_storage_area_m2,communal_area_separated_or_screened};yes
- `C2.4.3-r1` Waste management plan for apartments;j;=;-;judgment ⚑

## 2.5 Utilities (coding all; fb M2.5)
- `C2.5.1` Service utilities accessible, with clear …;c;=;services.service_utilities_accessible_screened;yes
- `C2.5.2` Functional utilities behind primary street …;c;=;services.{functional_utilities_behind_setback,functional_utilities_not_visible_from_street};all(yes; yes)

## 2.6 Outbuildings (coding all; fb M2.6)
- `C2.6.1` Outbuilding area, ridge height and location …;m;=;4 facts: outbuilding.{present,total_area_m2};all(<= 60.0 m²; <= 4.2 m; no)
- `C2.6.1-r1` Outbuilding wall height;m;=;3 facts: outbuilding.{present,wall_height_m};<= 3.0 m;exc 1: C2.6.2 ⚑

## 2.7 Universal design (coding all; fb M2.7)
- `C2.7.1` Ten or more apartments: at least 20% of …;m;=;proposal.{dwelling_count,dwellings_universal_design_pct};>= 20%
- `C2.7.2` Gold-level universal design dwelling seeking …;m;=;3 facts: proposal.{seeks_universal_design_site_area_variation,universal_design_level};all(== gold; <= 90.0 m²)

## 2.8 Ancillary dwellings (coding all; fb M2.8)
- `C2.8.1` Ancillary dwelling: dual key only, number …;m;=;5 facts: proposal.{ancillary_dwelling,dwelling_count};all of 3 tests ⚑

## 2.9 Small dwellings (coding all; fb M2.9)
- `C2.9.1` Small dwelling subject to site area …;m;=;proposal.{small_dwelling,internal_floor_area_m2};<= 60.0 m² ⚑

## 3.1 Site cover (coding all; fb M3.1)
- `C3.1.1` Maximum site cover;m;=;building.roofed_area_m2, site.area_m2;<= Table 3.1a by coding of …

## 3.2 Building height (coding all; fb M3.2)
- `C3.2.1#height` Maximum total building height;m;=;building.total_height_m;<= Table 3.2a-height
- `C3.2.1#storeys` Maximum number of storeys;m;=;proposal.storeys;<= Table 3.2a-storeys

## 3.3 Street setbacks (coding all; fb M3.3)
- `C3.3.1` Primary street setback;m;=;building.primary_street_setback_m;>= Table 3.3a-primary
- `C3.3.1#communal-street` Setback to communal street: no provision in …;j;=;site.has_communal_street, building.communal_street_setback_m;judgment ⚑
- `C3.3.1#laneway` Setback to adjoining laneway or right-of-way that is not primary …;m;=;3 facts: building.row_setback_m, site.has_row;>= Table 3.3a-laneway
- `C3.3.1#laneway-primary` Setback to adjoining laneway or right-of-way that is primary street;m;=;3 facts: building.row_setback_m, site.has_row;>= Table 3.3a-laneway-primary
- `C3.3.1#r1` Minor projections into street setback;m;=;building.primary_street_projection_m;<= 0.75 m
- `C3.3.1#secondary` Secondary street setback;m;=;building.secondary_street_setback_m, site.has_secondary_street;>= Table 3.3a-secondary
- `C3.3.2(i)` Reduced primary street setback for portion of frontage: minimum …;m;R10-R40;building.{primary_street_setback_reduced_portion_m,primary_street_reduced_portion_width_m};>= Table 3.3b
- `C3.3.2(i)#r1` Reduced primary street setback for portion of frontage: maximum …;m;R10-R40;building.primary_street_reduced_portion_width_m, site.frontage_m;max(0.3 * site.frontage_m, 4) >= …
- `C3.3.2(ii)` Porch, verandah or unenclosed balcony …;m;=;building.porch_projection_m;2 * building.porch_projection_m <= …
- `C3.3.2(iii)` Corner lot subdivision: reduced setback to …;m;R15-R60;building.primary_street_setback_m, site.corner_lot_subdivided;>= 2.5 m ⚑
- `C3.3.2(iii)#r1` Corner lot subdivision: porch, balcony or …;m;R15-R60;building.porch_street_setback_m, site.corner_lot_subdivided;>= 1.5 m ⚑
- `C3.3.3` Garage setback from primary street;m;R10-R35;5 facts: parking.garage.setback_primary_m, site.verge.path_or_road_offset_m;>= 5.0 m;exc 2: footpath or road …,garage allows …
- `C3.3.3#r40-plus` Garage setback from primary street, R40 and …;m;R40-R60;parking.garage.{setback_primary_m,present};>= Table 3.3a-primary
- `C3.3.4` Carport setback from primary street;m;=;6 facts: parking.carport.{setback_primary_m,present};>= Table 3.3a-primary;exc 1: carport 50 per …
- `C3.3.5#carport-row` Carport setback from right-of-way;m;=;4 facts: parking.carport.{setback_row_m,present};>= Table 3.3a-laneway
- `C3.3.5#carport-secondary` Carport setback from secondary street;m;=;3 facts: parking.carport.{setback_secondary_m,present};>= Table 3.3a-secondary
- `C3.3.5#garage-row` Garage setback from right-of-way;m;=;4 facts: parking.garage.{setback_row_m,present};>= Table 3.3a-laneway
- `C3.3.5#garage-secondary` Garage setback from secondary street;m;=;3 facts: parking.garage.{setback_secondary_m,present};>= Table 3.3a-secondary

## 3.4 Lot boundary setbacks (coding all; fb M3.4)
- `C3.4.1#rear` Rear setback (R10-R15);m;R10-R15;building.rear_setback_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-rear;exc 1: adjoining … ⚑
- `C3.4.1#rear-r17.5` Rear setback (R17.5 and above): no provision;m;R17.5-R60;building.rear_setback_m;>= Table 3.4a-rear ⚑
- `C3.4.1#side-3.6-to-7m` Side setback, walls 3.6 m to 7 m high (R10-R25);m;R10-R25;3 facts: building.side_setback_walls_3_6_to_7m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-3.6-to-7m;exc 1: adjoining … ⚑
- `C3.4.1#side-3.6-to-7m-r30-r60` Side setback, walls 3.6 m to 7 m high (R30-R60);m;R30-R60;building.{side_setback_walls_3_6_to_7m_m,has_walls_3_6_to_7m};>= Table 3.4a-side-3.6-to-7m ⚑
- `C3.4.1#side-over-7.1m` Side setback, walls above 7.1 m high (R10-R25);m;R10-R25;3 facts: building.side_setback_walls_over_7_1m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-over-7.1m;exc 1: adjoining … ⚑
- `C3.4.1#side-over-7.1m-r30-r60` Side setback, walls above 7.1 m high (R30-R60);m;R30-R60;building.{side_setback_walls_over_7_1m_m,has_walls_over_7_1m};>= Table 3.4a-side-over-7.1m ⚑
- `C3.4.1#side-to-3.5m` Side setback, walls up to 3.5 m high (R10-R25);m;R10-R25;3 facts: building.side_setback_walls_to_3_5m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-to-3.5m;exc 1: adjoining …
- `C3.4.1#side-to-3.5m-r30-r60` Side setback, walls up to 3.5 m high (R30-R60);m;R30-R60;building.{side_setback_walls_to_3_5m_m,has_walls_to_3_5m};>= Table 3.4a-side-to-3.5m
- `C3.4.1(i)` Minor projections into lot boundary setback;m;=;building.side_projection_m;<= 0.75 m
- `C3.4.2` Second and third storey walls: maximum 14 m …;m;=;4 facts: building.{upper_storey_wall_max_length_m,upper_storey_wall_over_14m_setback_m};any(<= 14 m; >= 3 m; yes)
- `C3.4.3` Carports, patios, verandahs or equivalent …;m;=;5 facts: building.boundary_structure.{present,length_m};all(<= 10 m; <= 3 m; <= 4.2 m; <= …
- `C3.4.4#count-r10-r17.5` Boundary walls on one lot boundary only …;m;R10-R17.5;building.boundary_walls.count;<= 1
- `C3.4.4#count-r20-r25` Boundary walls on up to two lot boundaries, R20-R25;m;R20-R25;building.boundary_walls.count;<= 2
- `C3.4.4#count-r30-r40-narrow` Boundary walls on up to two lot boundaries, R30-R40 narrow lots with …;m;R30-R40;3 facts: building.boundary_walls.count, site.frontage_m;<= 2
- `C3.4.4#height-r10-r40` Boundary wall maximum height, R10-R40;m;R10-R40;3 facts: building.boundary_walls.{max_height_m,count};<= 3.5 m;exc 1: abuts an existing …
- `C3.4.4#height-r50` Boundary wall maximum height, R50 and above;m;R50-R60;3 facts: building.boundary_walls.{max_height_m,count};<= 7 m;exc 1: abuts an existing …
- `C3.4.4#length-r10-r17.5` Boundary wall maximum length, R10-R17.5;m;R10-R17.5;3 facts: building.boundary_walls.{max_length_m,count};<= 9 m;exc 1: abuts an existing …
- `C3.4.4#length-r20-r25` Boundary wall maximum length, R20-R25;m;R20-R25;4 facts: building.boundary_walls.{max_length_m,max_pct_of_boundary};any(<= 9 m; <= 35);exc 1: abuts an existing …
- `C3.4.4#length-r30-r40` Boundary wall maximum length, R30-R40 all …;m;R30-R40;5 facts: building.boundary_walls.{max_pct_of_boundary,count};<= 65;exc 1: abuts an existing … ⚑
- `C3.4.4#length-r30-r40-narrow` Boundary wall maximum length, R30-R40 narrow …;m;R30-R40;5 facts: building.boundary_walls.{excl_adjoining_pos_pct,count};<= 80%;exc 1: abuts an existing …
- `C3.4.4#length-r50` Boundary wall maximum length, R50 and above;m;R50-R60;5 facts: building.boundary_walls.{max_length_m,beyond_14m_setback_m};any(<= 14 m; all(>= 3 m; >= 3 m));exc 1: abuts an existing …
- `C3.4.4#length-r50-wide` Boundary wall cumulative length, R50 and …;m;R50-R60;4 facts: building.boundary_walls.{max_pct_of_boundary,count};<= 65;exc 1: abuts an existing … ⚑
- `C3.4.4#r1` Lower density code governs boundary wall …;j;=;-;judgment
- `C3.4.4#r2` Retaining wall beneath boundary wall is …;j;=;-;judgment
- `C3.4.4(i)` Boundary walls located behind street setback;c;=;building.boundary_walls.{behind_street_setback,count};yes
- `C3.4.4(ii)` Boundary wall overshadowing within C3.8.1;j;=;-;judgment
- `C3.4.4(iii)` Boundary walls finished to equivalent …;j;=;-;judgment
- `C3.4.5` Boundary wall abutting existing or …;j;=;-;judgment
- `C3.4.6` Separation between buildings, or facing …;m;=;3 facts: building.{separation_same_lot_m,separation_same_lot_wall_height_m};>= Table 3.4a-separation by … ⚑

## 3.5 Site works and retaining walls (coding all; fb M3.5)
- `C3.5.1` Site works forward of street setback line;m;=;site_works.{forward_of_setback_for_access_drainage_light,forward_of_setback_max_change_m};<= 0.5 m;exc 1: necessary for …
- `C3.5.2` Retaining walls and fill behind street …;m;=;site_works.{retaining_max_height_m,retaining_setback_m};>= Table 3.5a by …
- `C3.5.3` Excavation behind street setback line may …;c;=;site_works.excavation_behind_setback;yes

## 3.6 Streetscape (coding all; fb M3.6)
- `C3.6.1` Upper-level balconies or windows overlook …;c;=;building.{storeys,upper_level_overlook_street};yes
- `C3.6.1-r1` Upper-level outlook to adjoining public open …;c;=;3 facts: building.{storeys,upper_level_outlook_to_pos};yes ⚑
- `C3.6.2` Ground-floor apartments fronting street have …;c;=;building.ground_floor_apartments_separate_entry;yes
- `C3.6.3` Garage width as proportion of frontage;m;=;5 facts: parking.garage.{entrance_clearly_visible,ext_width_m};<= 50% of site.frontage_m;exc 1: upper floor or …
- `C3.6.4` Carport width as proportion of frontage;m;=;3 facts: parking.carport.{present,width_m};<= 60% of site.frontage_m ⚑
- `C3.6.5(i)` Front fence or wall maximum height 1.8 m;m;=;building.front_fence.{height_m,present};<= 1.8 m
- `C3.6.5(ii)` Front fence or wall visually permeable above …;m;=;building.front_fence.{permeable_above_m,present};<= 1.2 m
- `C3.6.6-r1` Front fence solid pillars maximum height 1.8 …;m;=;3 facts: building.front_fence.{pillar_height_m,pillars_present};<= 1.8 m
- `C3.6.6-r2` Front fence solid pillars maximum 450 mm by …;m;=;3 facts: building.front_fence.{pillar_size_mm,pillars_present};<= 450 mm

## 3.7 Access (coding all; fb M3.7)
- `C3.7.1` Vehicle access from lowest-order available …;c;=;4 facts: parking.access.from_lowest_order_street, site.has_communal_street;yes
- `C3.7.2` One vehicle access point per lot;m;=;5 facts: parking.access.count, proposal.retained_dwelling;<= 1;exc 3: (i) retained …,(ii) dwellings …,(iii) lot frontage … ⚑
- `C3.7.3(i)` Driveway minimum width 3 m;m;=;parking.driveway.width_min_m;>= 3.0 m
- `C3.7.3(ii)` Driveway maximum width 6 m at street …;m;=;parking.driveway.width_at_boundary_m;<= 6.0 m
- `C3.7.3(iii)` Driveway set back 0.3 m from side lot …;m;=;parking.driveway.side_boundary_setback_m;>= 0.3 m
- `C3.7.3(iv)` Driveway set back 6 m from street corner;m;=;parking.driveway.setback_to_corner_m, site.corner_lot;>= 6.0 m
- `C3.7.3(v)` Driveway at right angles to road carriageway;c;=;parking.driveway.right_angle_to_carriageway;yes
- `C3.7.3(vi)` Driveway adequately trafficable and drained;c;=;parking.driveway.trafficable_and_drained;yes
- `C3.7.4` Exit to street in forward gear;c;=;4 facts: parking.driveway.{dwellings_served,exit_forward_gear};yes
- `C3.7.5` Passing points on driveways serving five or …;c;=;parking.driveway.dwellings_served, site.communal_street_passing_bay;yes ⚑
- `C3.7.6` Simultaneous entry and exit on primary …;c;=;site.{communal_street_passing_bay,primary_street_class};yes ⚑
- `C3.7.7` Sightline truncation at driveways, ROWs and …;c;=;parking.sightlines.clear_0_75m_within_1_5m, site.verge.path_or_road_offset_m;yes;exc 1: C3.7.8
- `C3.7.9` 1 m x 1 m sightline truncation either side …;c;=;3 facts: parking.access.street_type, parking.sightlines.row_truncation_1m;yes ⚑
- `C3.7.10` Legible, continuous pedestrian path from …;c;=;parking.path_of_travel_to_entries;yes
- `C3.7.11(i)` Pedestrian path minimum 1 m wide;m;=;parking.pedestrian_access_width_m, site.has_communal_street;>= 1.0 m
- `C3.7.11(ii)` Pedestrian path clearly delineated or …;c;=;parking.pedestrian_access_separate, site.has_communal_street;yes
- `C3.7.11(iii)` Pedestrian path continuous from street …;c;=;parking.pedestrian_path_continuous, site.has_communal_street;yes
- `C3.7.12(i)` Pedestrian access leg minimum width 1.5 m;m;=;3 facts: proposal.retained_dwelling, site.has_pedestrian_access_leg;>= 1.5 m;exc 1: reduced to 1 m …
- `C3.7.12(ii)` Pedestrian access leg continuous 1 m clear …;m;=;site.{has_pedestrian_access_leg,pedestrian_access_leg_clear_path_m};>= 1.0 m
- `C3.7.13` Communal street or battleaxe leg minimum …;m;=;3 facts: site.{battleaxe,communal_street_width_m};>= 3.6 m
- `C3.7.14` Communal street or battleaxe leg lighting …;j;=;-;judgment

## 3.8 Solar access for adjoining sites (coding all; fb M3.8)
- `C3.8.1` Maximum overshadowing of adjoining property;m;=;5 facts: adjoining.south.{frontage_m,r_code};<= Table 3.8a by coding;exc 1: C3.8.2
- `C3.8.1-diagonal` Maximum overshadowing of diagonally adjacent …;m;=;3 facts: adjoining.diagonal.r_code, overshadow.diagonal_pct;<= Table 3.8a-diagonal by coding
- `C3.8.2` Overshadowing of narrow adjoining lot;m;=;5 facts: adjoining.south.{battleaxe,frontage_m};<= Table 3.8b by coding,frontage_m
- `C3.8.3` Proportional shading limit where neighbour's …;c;=;3 facts: adjoining.north_shared_boundary_count, overshadow.proportional_to_shared_boundary;yes

## 3.9 Visual privacy (coding all; fb M3.9)
- `C3.9.1-r1` Cone of vision setback from bedroom or study …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m;exc 1: cone of vision …
- `C3.9.1-r2` Cone of vision setback from other habitable …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 4.5 m;exc 1: cone of vision …
- `C3.9.1-r3` Cone of vision setback from outdoor active …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 6.0 m;exc 1: cone of vision …
- `C3.9.2` Screening where cone of vision captures …;c;=;5 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;yes;exc 1: cone falls forward …
- `C3.9.3` Bedroom or study major opening offset 1.5 m …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_offset_m;>= 1.5 m
- `C3.9.4` Apartments on same lot apply C3.9.1 to …;c;=;privacy.between_apartments_same_lot_compliant;yes
- `C3.9.5-r1` Vacant or unknown adjoining site: cone from bedroom or study opening …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m;exc 1: C3.9.6
- `C3.9.5-r2` Vacant or unknown adjoining site: cone from other habitable room …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.other_habitable_setback_m;>= 4.5 m;exc 1: C3.9.6
- `C3.9.5-r3` Vacant or unknown adjoining site: cone from outdoor active habitable …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.outdoor_active_setback_m;>= 6.0 m;exc 1: C3.9.6

## 4.1 Site area (coding all; fb M4.1)
- `C4.1.1` Average site area per apartment;m;=;8 facts: site.area_m2, subdivision.truncation_area_added_m2;(site.area_m2 + …;exc 6: C4.1.3,C4.1.4,C4.1.5,C4.1.6,C4.1.7 ⚑
- `C4.1.2` Corner truncation: up to 20 m2 added to …;j;=;-;judgment
- `M4.1.2` WAPC approval of lots with average site area …;j/M;=;-;judgment
- `M4.1.2-r1` Potential change: local government approval …;j/M;=;-;judgment
- `M4.1.3` Decision-maker may approve strata lot of …;j/M;R40-R60;-;judgment
- `M4.1.4` WAPC approval of survey-strata or strata …;j/M;=;-;judgment
