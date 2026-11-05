# Chapter 2 Single Houses: digest

Version draft-2026-10-24. Applies to single_house; coding all; pathway deemed-exempt-or-merit. 151 provisions, 26 flagged ⚑.
Testable column C; a provision not met falls back to the element's M record. Full text: `elements/ch2/<element>.md`.

Line, fields split by `;`: `ID` title; kind (m measurable, c conditional, j judgment; /col if not C); coding (= as heading); facts (count and the first two; the full list is under the provision's heading in the pack); test (a table is looked up by coding unless `by` says otherwise); exc n: labels; fb (fallback) if not the element's; ⚑ verify. `site.r_code` is implied by every coding and is not counted.
Find a provision in its pack by grepping for its heading, e.g. ``^### `C3.3.1` ``, and read that section only.

Note: R80 standards apply to single houses in areas coded R100, R160, LR, MR and HR (Chapter 2 note; register CH1-06). R100-SL provisions are modified by Table 2.10a.

## 1.1 Private open space (coding R50+,LR,MR,HR; fb M1.1)
- `C1.1.1` Outdoor living area minimum area;m;R2-R40;landscape.ola.area_m2;>= Table 1.1a
- `C1.1.1-r1` Outdoor living area minimum dimension 4 m;m;R17.5-R40;landscape.ola.min_dim_m;>= 4 m
- `C1.1.1-r2` Outdoor living area: 65% of required area …;m;R17.5-R40;landscape.ola.uncovered_pct;>= 65%
- `C1.1.1-r3` Outdoor living area behind street setback …;c;R2-R40;3 facts: landscape.ola.{behind_street_setback,in_primary_street_setback};yes;exc 1: C1.1.2
- `C1.1.2` Outdoor living area within primary street …;c;R2-R40;landscape.ola.in_primary_street_setback, building.front_fence.visually_permeable;yes
- `C1.1.3` Primary garden area minimum area;m;=;8 facts: landscape.pga.area_m2, site.area_m2;>= Table 1.1b by area_m2;exc 1: C1.1.4
- `C1.1.3-r1` Primary garden area minimum dimension 3 m;m;=;landscape.pga.min_dim_m;>= 3 m
- `C1.1.3-r2` Primary garden area maximum permanent roof …;m;=;landscape.pga.roofed_pct;<= 35%
- `C1.1.3-r3` Primary garden area behind street setback …;c;=;3 facts: landscape.pga.{behind_street_setback,in_primary_street_setback};yes;exc 1: C1.1.5
- `C1.1.3-r100sl` Primary garden area for lots coded R100-SL;m;R100-SL;3 facts: landscape.pga.{area_m2,min_dim_m};all(>= 15 m²; >= 3 m; <= 0%)
- `C1.1.5` Primary garden area within primary street …;c;R50+,R100-SL,LR,MR,HR;landscape.pga.in_primary_street_setback, building.front_fence.visually_permeable;yes

## 1.2 Trees and landscaping (coding R2+,LR,MR,HR; fb M1.2)
- `C1.2.1` Soft landscaping minimum 15% of site;m;=;3 facts: landscape.soft_area_m2, site.area_m2;>= 15% of site.area_m2;exc 1: C1.2.4
- `C1.2.1-r1` Soft landscaping minimum dimension 1 m;m;=;landscape.soft_min_dim_m;>= 1 m
- `C1.2.1-r100sl` Soft landscaping for lots coded R100-SL: 10% …;m;R100-SL;3 facts: landscape.soft_area_m2, site.area_m2;all(>= 10% of site.area_m2; >= 1 m)
- `C1.2.2` Primary street setback area minimum 30% soft …;m;=;landscape.{street_setback_soft_area_m2,street_setback_area_m2};>= 30% of …
- `C1.2.3` Small trees in primary street setback area;m;=;3 facts: landscape.trees_in_street_setback, site.frontage_m;>= Table 1.2a by frontage_m ⚑
- `C1.2.3-r1` One small tree per dwelling elsewhere on lot;m;=;4 facts: landscape.{trees_elsewhere,trees_in_street_setback};>= 1;exc 2: per-dwelling tree … ⚑
- `C1.2.3-r2` Deep soil area per required small tree;m;=;landscape.{tree_deep_soil_min_m2,tree_deep_soil_min_dim_m};all(>= 9 m²; >= 1.5 m)
- `C1.2.5` Nominal root zone for retained significant …;c;all;site.{significant_tree_retained,retained_tree_root_zone_provided};yes

## 1.3 Water management and conservation (coding all; fb M1.3)
- `C1.3.1` Stormwater from small rainfall event …;c;=;landscape.{stormwater_retained_on_site,stormwater_to_system_required};yes;exc 1: C1.3.2

## 2.1 Size and layout of dwellings (coding all; fb M2.1)
- `C2.1.1(i)` Primary living space on ground floor has …;c;=;proposal.primary_living_space_floor, building.primary_living_direct_access_to_pga;yes ⚑
- `C2.1.1(ii)` Primary living space on upper floor has …;m;=;5 facts: proposal.primary_living_space_floor, building.primary_living_direct_access_to_upper_pos;all of 3 tests ⚑
- `C2.1.2` Dedicated weatherproof storage area per …;m;R50+,R100-SL;5 facts: building.storage.{area_m2,min_dim_m};all of 4 tests

## 2.2 Solar access and natural ventilation (coding R50+,R100-SL; fb M2.2)
- `C2.2.1` Courtyard that is only daylight source to …;m;=;3 facts: building.{courtyard_daylight_only,courtyard_open_to_sky};all(yes; >= 4.0 m²)
- `C2.2.2` Major opening to primary living space …;m;=;5 facts: site.climate_zone, building.primary_living_major_opening_orientation;all of 3 tests;exc 1: transitional

## 2.3 Parking (coding all; fb M2.3)
- `C2.3.1` Minimum on-site car parking spaces, Perth and Peel;m;=;3 facts: parking.spaces, site.location;>= Table 2.3a by location,bedrooms
- `C2.3.1-r1` Minimum parking for ancillary dwelling, Perth and Peel;m;=;proposal.ancillary_dwelling, parking.ancillary_spaces;>= 0
- `C2.3.1-r2` Maximum garage and carport parking spaces …, Perth and Peel;m;R50+;parking.garage_carport_spaces, proposal.bedrooms;any(all(<= 1; <= 1); all(>= 2; <= …
- `C2.3.1-r3` Maximum garage and carport parking for …, Perth and Peel;m;R50+;proposal.ancillary_dwelling, parking.ancillary_garage_carport_spaces;<= 1
- `C2.3.2` Car spaces and manoeuvring areas per …, Perth and Peel;c;=;parking.as2890_compliant;yes
- `C2.3.3` Minimum on-site car parking spaces, R40 and …, regional;m;R2-R40;parking.spaces, proposal.bedrooms;>= Table 2.3b by bedrooms
- `C2.3.3-r1` Minimum parking for ancillary dwelling, R40 …, regional;m;R2-R40;proposal.ancillary_dwelling, parking.ancillary_spaces;>= 1
- `C2.3.3-r2` Maximum garage and carport parking, R50 and …, regional;m;R50+;parking.garage_carport_spaces;<= 1 ⚑
- `C2.3.3-r3` Maximum garage and carport parking for …, regional;m;R50+;proposal.ancillary_dwelling, parking.ancillary_garage_carport_spaces;<= 0 ⚑
- `C2.3.4` Car spaces and manoeuvring areas per …, regional;c;=;parking.as2890_compliant;yes

## 2.4 Waste management (coding all; fb M2.4)
- `C2.4.1` Waste storage bins screened from view;c;=;services.bins_screened;yes

## 2.5 Utilities (coding all; fb M2.5)
- `C2.5.1` Service utilities accessible, with clear …;c;=;services.service_utilities_accessible_screened;yes
- `C2.5.2` Functional utilities behind primary street …;c;=;services.{functional_utilities_behind_setback,functional_utilities_not_visible_from_street};all(yes; yes)

## 2.6 Outbuildings (coding all; fb M2.6)
- `C2.6.1` Outbuilding area, ridge height and location …;m;=;4 facts: outbuilding.{present,total_area_m2};all(<= 60.0 m²; <= 4.2 m; no)
- `C2.6.1-r1` Outbuilding wall height;m;=;3 facts: outbuilding.{present,wall_height_m};<= 3.0 m;exc 1: C2.6.2 ⚑

## 2.7 Universal design (coding all; fb M2.7)
- `C2.7.1` Gold-level universal design dwelling seeking …;m;=;3 facts: proposal.{seeks_universal_design_site_area_variation,universal_design_level};all(== gold; <= 110.0 m²)

## 2.8 Ancillary dwellings (coding all; fb M2.8)
- `C2.8.1` Ancillary dwelling: maximum one per site and …;m;=;4 facts: proposal.ancillary_dwelling, ancillary.count;all of 2 tests

## 2.9 Small dwellings (coding all; fb M2.9)
- `C2.9.1` Small dwelling subject to site area …;m;=;proposal.{small_dwelling,internal_floor_area_m2};<= 70.0 m²

## 2.10 Housing on lots less than 100m2 (coding R100-SL; fb M2.10)
- `C2.10.1(i)` R100-SL dwelling fronts primary street …;c;=;site.area_m2, building.fronts_street_or_row;yes ⚑
- `C2.10.1(ii)` R100-SL dwelling: all R-Codes provisions …;j;=;-;judgment ⚑

## 3.1 Site cover (coding all; fb M3.1)
- `C3.1.1` Maximum site cover;m;=;building.roofed_area_m2, site.area_m2;<= Table 3.1a by coding of …

## 3.2 Building height (coding all; fb M3.2)
- `C3.2.1#height` Maximum total building height;m;=;building.total_height_m;<= Table 3.2a-height
- `C3.2.1#storeys` Maximum number of storeys;m;R2+,LR,MR,HR;proposal.storeys;<= Table 3.2a-storeys
- `C3.2.1#storeys-r100sl` Storeys on lots less than 100 m2 (R100-SL) …;m;R100-SL;proposal.storeys;all(>= 2; <= 4)

## 3.3 Street setbacks (coding R2+,LR,MR,HR; fb M3.3)
- `C3.3.1` Primary street setback;m;=;building.primary_street_setback_m;>= Table 3.3a-primary
- `C3.3.1#laneway` Setback to adjoining laneway or right-of-way that is not primary …;m;=;3 facts: building.row_setback_m, site.has_row;>= Table 3.3a-laneway
- `C3.3.1#laneway-primary` Setback to adjoining laneway or right-of-way that is primary street;m;=;3 facts: building.row_setback_m, site.has_row;>= Table 3.3a-laneway-primary
- `C3.3.1#laneway-r100sl` Setback to adjoining right-of-way on lots …;m;R100-SL;building.row_setback_m, site.has_row;>= 0.5 m ⚑
- `C3.3.1#primary-r100sl` Primary street setback on lots less than 100 …;m;R100-SL;building.primary_street_setback_m;>= 1.0 m
- `C3.3.1#r1` Minor projections into street setback;m;all;building.primary_street_projection_m;<= 0.75 m
- `C3.3.1#secondary` Secondary street setback;m;=;building.secondary_street_setback_m, site.has_secondary_street;>= Table 3.3a-secondary
- `C3.3.1#secondary-r100sl` Secondary street setback on lots less than …;m;R100-SL;building.secondary_street_setback_m, site.has_secondary_street;>= 1.0 m
- `C3.3.2(i)` Reduced primary street setback for portion of frontage: minimum …;m;R2-R40;building.{primary_street_setback_reduced_portion_m,primary_street_reduced_portion_width_m};>= Table 3.3b
- `C3.3.2(i)#r1` Reduced primary street setback for portion of frontage: maximum …;m;R2-R40;building.primary_street_reduced_portion_width_m, site.frontage_m;max(0.3 * site.frontage_m, 4) >= …
- `C3.3.2(ii)` Porch, verandah or unenclosed balcony …;m;=;building.porch_projection_m;2 * building.porch_projection_m <= …
- `C3.3.2(iii)` Corner lot subdivision: reduced setback to …;m;R15+,LR,MR,HR;building.primary_street_setback_m, site.corner_lot_subdivided;>= 2.5 m
- `C3.3.2(iii)#r1` Corner lot subdivision: porch, balcony or …;m;R15+,LR,MR,HR;building.porch_street_setback_m, site.corner_lot_subdivided;>= 1.5 m
- `C3.3.3` Garage setback from primary street;m;R2-R35;5 facts: parking.garage.setback_primary_m, site.verge.path_or_road_offset_m;>= 5.0 m;exc 2: footpath or road …,garage allows …
- `C3.3.3#r40-plus` Garage setback from primary street, R40 and …;m;R40+,LR,MR,HR;parking.garage.{setback_primary_m,present};>= Table 3.3a-primary
- `C3.3.4` Carport setback from primary street;m;=;6 facts: parking.carport.{setback_primary_m,present};>= Table 3.3a-primary;exc 1: carport 50 per …
- `C3.3.5#carport-row` Carport setback from right-of-way;m;=;4 facts: parking.carport.{setback_row_m,present};>= Table 3.3a-laneway
- `C3.3.5#carport-secondary` Carport setback from secondary street;m;=;3 facts: parking.carport.{setback_secondary_m,present};>= Table 3.3a-secondary
- `C3.3.5#garage-row` Garage setback from right-of-way;m;=;4 facts: parking.garage.{setback_row_m,present};>= Table 3.3a-laneway
- `C3.3.5#garage-secondary` Garage setback from secondary street;m;=;3 facts: parking.garage.{setback_secondary_m,present};>= Table 3.3a-secondary

## 3.4 Lot boundary setbacks (coding all; fb M3.4)
- `C3.4.1#rear` Rear setback (R2-R15);m;R2-R15;building.rear_setback_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-rear;exc 1: adjoining …
- `C3.4.1#rear-r17.5` Rear setback (R17.5 and above): no provision;m;R17.5+,R100-SL,LR,MR,HR;building.rear_setback_m;>= Table 3.4a-rear ⚑
- `C3.4.1#side-3.6-to-7m` Side setback, walls 3.6 m to 7 m high (R2-R40);m;R2-R40;3 facts: building.side_setback_walls_3_6_to_7m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-3.6-to-7m;exc 1: adjoining … ⚑
- `C3.4.1#side-3.6-to-7m-r50` Side setback, walls 3.6 m to 7 m high (R50 and above);m;R50+,R100-SL,LR,MR,HR;building.{side_setback_walls_3_6_to_7m_m,has_walls_3_6_to_7m};>= Table 3.4a-side-3.6-to-7m ⚑
- `C3.4.1#side-over-7.1m` Side setback, walls above 7.1 m high (R2-R40);m;R2-R40;3 facts: building.side_setback_walls_over_7_1m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-over-7.1m;exc 1: adjoining … ⚑
- `C3.4.1#side-over-7.1m-r50` Side setback, walls above 7.1 m high (R50 and above);m;R50+,R100-SL,LR,MR,HR;building.{side_setback_walls_over_7_1m_m,has_walls_over_7_1m};>= Table 3.4a-side-over-7.1m ⚑
- `C3.4.1#side-to-3.5m` Side setback, walls up to 3.5 m high (R2-R40);m;R2-R40;3 facts: building.side_setback_walls_to_3_5m_m, site.adjoining_pedestrian_access_way_width_m;>= Table 3.4a-side-to-3.5m;exc 1: adjoining …
- `C3.4.1#side-to-3.5m-r50` Side setback, walls up to 3.5 m high (R50 and above);m;R50+,R100-SL,LR,MR,HR;building.{side_setback_walls_to_3_5m_m,has_walls_to_3_5m};>= Table 3.4a-side-to-3.5m
- `C3.4.1(i)` Minor projections into lot boundary setback;m;=;building.side_projection_m;<= 0.75 m
- `C3.4.2` Second and third storey walls: maximum 14 m …;m;R2+,LR,MR,HR;4 facts: building.{upper_storey_wall_max_length_m,upper_storey_wall_over_14m_setback_m};any(<= 14 m; >= 3 m; yes)
- `C3.4.3` Carports, patios, verandahs or equivalent …;m;=;5 facts: building.boundary_structure.{present,length_m};all(<= 10 m; <= 3 m; <= 4.2 m; <= …
- `C3.4.4#count-r10-r17.5` Boundary walls on one lot boundary only …;m;R10-R17.5;building.boundary_walls.count;<= 1
- `C3.4.4#count-r20-r25` Boundary walls on up to two lot boundaries, R20-R25;m;R20-R25;building.boundary_walls.count;<= 2
- `C3.4.4#count-r30-r40-narrow` Boundary walls on up to two lot boundaries, R30-R40 narrow lots with …;m;R30-R40;3 facts: building.boundary_walls.count, site.frontage_m;<= 2
- `C3.4.4#height-r10-r40` Boundary wall maximum height, R10-R40;m;R10-R40;3 facts: building.boundary_walls.{max_height_m,count};<= 3.5 m;exc 1: abuts an existing …
- `C3.4.4#height-r50` Boundary wall maximum height, R50 and above;m;R50+,LR,MR,HR;3 facts: building.boundary_walls.{max_height_m,count};<= 7 m;exc 1: abuts an existing …
- `C3.4.4#height-r100sl` Boundary wall maximum height on lots less …;m;R100-SL;3 facts: building.boundary_walls.{max_height_m,count};<= 13 m ⚑
- `C3.4.4#length-r10-r17.5` Boundary wall maximum length, R10-R17.5;m;R10-R17.5;3 facts: building.boundary_walls.{max_length_m,count};<= 9 m;exc 1: abuts an existing …
- `C3.4.4#length-r20-r25` Boundary wall maximum length, R20-R25;m;R20-R25;4 facts: building.boundary_walls.{max_length_m,max_pct_of_boundary};any(<= 9 m; <= 35);exc 1: abuts an existing …
- `C3.4.4#length-r30-r40` Boundary wall maximum length, R30-R40 all …;m;R30-R40;5 facts: building.boundary_walls.{max_pct_of_boundary,count};<= 65;exc 1: abuts an existing …
- `C3.4.4#length-r30-r40-narrow` Boundary wall maximum length, R30-R40 narrow …;m;R30-R40;5 facts: building.boundary_walls.{excl_adjoining_pos_pct,count};<= 80%;exc 1: abuts an existing …
- `C3.4.4#length-r50` Boundary wall maximum length, R50 and above;m;R50+,LR,MR,HR;5 facts: building.boundary_walls.{max_length_m,beyond_14m_setback_m};any(<= 14 m; all(>= 3 m; >= 3 m));exc 1: abuts an existing …
- `C3.4.4#length-r50-wide` Boundary wall cumulative length, R50 and …;m;R50+,LR,MR,HR;4 facts: building.boundary_walls.{max_pct_of_boundary,count};<= 65;exc 1: abuts an existing … ⚑
- `C3.4.4#r1` Lower density code governs boundary wall …;j;=;-;judgment
- `C3.4.4#r2` Retaining wall beneath boundary wall is …;j;=;-;judgment
- `C3.4.4(i)` Boundary walls located behind street setback;c;=;building.boundary_walls.{behind_street_setback,count};yes
- `C3.4.4(ii)` Boundary wall overshadowing within C3.9.1;j;=;-;judgment
- `C3.4.4(iii)` Boundary walls finished to equivalent …;j;=;-;judgment
- `C3.4.5` Boundary wall abutting existing or …;j;=;-;judgment

## 3.5 Site works and retaining walls (coding all; fb M3.5)
- `C3.5.1` Site works forward of street setback line;m;=;site_works.{forward_of_setback_for_access_drainage_light,forward_of_setback_max_change_m};<= 0.5 m;exc 1: necessary for …
- `C3.5.2` Retaining walls and fill behind street …;m;=;site_works.{retaining_max_height_m,retaining_setback_m};>= Table 3.5a by …
- `C3.5.3` Excavation behind street setback line may …;c;=;site_works.excavation_behind_setback;yes

## 3.6 Streetscape (coding all; fb M3.6)
- `C3.6.1` Dwelling addresses street;c;=;building.{entrance_identifiable_from_street,major_opening_to_frontage};all(yes; yes)
- `C3.6.2` Upper-level outlook to adjoining public open …;c;=;3 facts: building.upper_level_outlook_to_pos, proposal.storeys;yes
- `C3.6.3` Garage width as proportion of frontage;m;=;5 facts: parking.garage.{entrance_clearly_visible,ext_width_m};<= 50% of site.frontage_m;exc 1: upper floor or … ⚑
- `C3.6.4` Carport width as proportion of frontage;m;=;3 facts: parking.carport.{present,width_m};<= 60% of site.frontage_m ⚑
- `C3.6.5(i)` Front fence or wall maximum height 1.8 m;m;all but R100-SL;building.front_fence.{height_m,present};<= 1.8 m
- `C3.6.5(i)-R100-SL` Street fence maximum height 900 mm;m;R100-SL;building.front_fence.{height_m,present};<= 0.9 m
- `C3.6.5(ii)` Front fence or wall visually permeable above …;m;=;building.front_fence.{permeable_above_m,present};<= 1.2 m
- `C3.6.6-r1` Front fence solid pillars maximum height 1.8 …;m;=;3 facts: building.front_fence.{pillar_height_m,pillars_present};<= 1.8 m
- `C3.6.6-r2` Front fence solid pillars maximum 450 mm by …;m;=;3 facts: building.front_fence.{pillar_size_mm,pillars_present};<= 450 mm

## 3.7 Access (coding all; fb M3.7)
- `C3.7.1` Vehicle access from lowest-order available …;c;=;4 facts: parking.access.from_lowest_order_street, site.has_communal_street;yes
- `C3.7.2` One vehicle access point per lot;m;R40+;5 facts: parking.access.count, proposal.retained_dwelling;<= 1;exc 3: (i) retained …,(ii) dwellings …,(iii) lot frontage … ⚑
- `C3.7.3(i)` Driveway minimum width 3 m;m;=;parking.driveway.width_min_m;>= 3.0 m
- `C3.7.3(ii)` Driveway maximum width 6 m at street …;m;=;parking.driveway.width_at_boundary_m;<= 6.0 m
- `C3.7.3(iii)` Driveway aggregate width 9 m per property;m;R2-R35;parking.driveway.aggregate_width_m;<= 9.0 m
- `C3.7.3(iv)` Driveway set back 6 m from street corner;m;=;parking.driveway.setback_to_corner_m, site.corner_lot;>= 6.0 m
- `C3.7.3(v)` Driveway at right angles to road carriageway;c;=;parking.driveway.right_angle_to_carriageway;yes
- `C3.7.3(vi)` Driveway adequately trafficable and drained;c;=;parking.driveway.trafficable_and_drained;yes
- `C3.7.4` Exit to street in forward gear;c;=;3 facts: parking.driveway.{exit_forward_gear,space_to_boundary_m};yes
- `C3.7.5` Sightline truncation at driveways, ROWs and …;c;=;parking.sightlines.clear_0_75m_within_1_5m, site.verge.path_or_road_offset_m;yes;exc 1: C3.7.6
- `C3.7.7` 1 m x 1 m sightline truncation either side …;c;=;parking.sightlines.row_truncation_1m, site.access_from_rear_row;yes ⚑
- `C3.7.8(i)` Pedestrian access leg minimum width 1.5 m;m;=;3 facts: proposal.retained_dwelling, site.has_pedestrian_access_leg;>= 1.5 m;exc 1: reduced to 1 m …
- `C3.7.8(ii)` Pedestrian access leg continuous 1 m clear …;m;=;site.{has_pedestrian_access_leg,pedestrian_access_leg_clear_path_m};>= 1.0 m
- `C3.7.9` Battleaxe leg minimum width 3.6 m;m;=;site.{battleaxe,battleaxe_leg_width_m};>= 3.6 m
- `C3.7.10` Battleaxe leg lighting and landscaping;j;=;-;judgment

## 3.8 Retaining existing dwellings (coding all; fb M3.8)
- `C3.8.1` Provisions that apply to retained dwelling;j;=;-;judgment

## 3.9 Solar access for adjoining sites (coding all but R100-SL; fb M3.9)
- `C3.9.1` Maximum overshadowing of adjoining property;m;=;6 facts: adjoining.south.r_code, building.max_wall_height_m;<= Table 3.9a by coding;exc 2: C3.9.2,C3.9.3
- `C3.9.1-diagonal` Maximum overshadowing of diagonally adjacent …;m;=;5 facts: adjoining.diagonal.r_code, building.max_wall_height_m;<= Table 3.9a-diagonal by coding;exc 1: C3.9.2
- `C3.9.3` Overshadowing of narrow adjoining lot;m;=;5 facts: adjoining.south.{battleaxe,frontage_m};<= Table 3.9b by coding,frontage_m
- `C3.9.4` Proportional shading limit where neighbour's …;c;=;3 facts: adjoining.north_shared_boundary_count, overshadow.proportional_to_shared_boundary;yes

## 3.10 Visual privacy (coding all but R100-SL; fb M3.10)
- `C3.10.1-r1` Cone of vision setback from bedroom or study …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m;exc 1: cone of vision …
- `C3.10.1-r2` Cone of vision setback from other habitable …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 4.5 m;exc 1: cone of vision …
- `C3.10.1-r3` Cone of vision setback from outdoor active …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;>= 6.0 m;exc 1: cone of vision …
- `C3.10.2` Screening where cone of vision captures …;c;=;5 facts: adjoining.vacant_or_unknown, privacy.cone_captures_adjoining_opening;yes;exc 1: cone falls forward …
- `C3.10.3` Bedroom or study major opening offset 1.5 m …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_offset_m;>= 1.5 m
- `C3.10.4-r1` Vacant or unknown adjoining site: cone from bedroom or study opening …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.bedroom_study_setback_m;>= 3.0 m;exc 1: C3.10.5
- `C3.10.4-r2` Vacant or unknown adjoining site: cone from other habitable room …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.other_habitable_setback_m;>= 4.5 m;exc 1: C3.10.5
- `C3.10.4-r3` Vacant or unknown adjoining site: cone from outdoor active habitable …;m;=;4 facts: adjoining.vacant_or_unknown, privacy.outdoor_active_setback_m;>= 6.0 m;exc 1: C3.10.5

## 4.1 Site area (coding all; fb M4.1)
- `C4.1.1` Minimum site area of site (Table 2B);m;=;7 facts: site.{area_m2,lot_approved_by_wapc};>= Table 2B-min;exc 5: C4.1.4,C4.1.5,C4.1.6,C4.1.7 ⚑
- `C4.1.1-r1` Average site area of proposed lots;m;=;7 facts: subdivision.{proposed,avg_site_area_m2};>= Table 2B-avg;exc 3: C4.1.5,C4.1.6,C4.1.7 ⚑
- `C4.1.1-r2` Minimum site area of rear battleaxe site;m;=;4 facts: site.{battleaxe,area_m2};>= Table 2B-battleaxe;exc 2: C4.1.4 ⚑
- `C4.1.1-r3` Minimum frontage of site (Table 2B);m;=;site.frontage_m;>= Table 2B-frontage
- `C4.1.1-r4` Minimum site area of proposed lots;m;=;6 facts: subdivision.{proposed,min_site_area_m2};>= Table 2B-min;exc 3: C4.1.5,C4.1.6,C4.1.7 ⚑
- `C4.1.1-r5` Minimum frontage of proposed lots;m;=;subdivision.{proposed,min_frontage_m};>= Table 2B-frontage
- `C4.1.1-r6` Minimum site area of proposed rear battleaxe …;m;=;3 facts: subdivision.{proposed,battleaxe_lot};>= Table 2B-battleaxe ⚑
- `C4.1.2` Calculation of minimum site area;j;=;-;judgment
- `M4.1.2` WAPC approval of lots up to 5% below Table …;j/M;=;-;judgment
- `C4.1.3` Adjustments to site area for truncations …;j;=;-;judgment
- `M4.1.3` WAPC approval of average site area variation …;j/M;R10-R35;-;judgment
- `M4.1.4` Potential change: greater subdivision …;j/M;R10-R17.5;-;judgment
- `M4.1.5` Potential change: minimum site area reduced …;j/M;=;-;judgment
