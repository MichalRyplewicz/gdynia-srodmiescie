# BUILDINGS IN THE CITY CENTER OF GDYNIA
Characteristics of the buildings in the centre: ground-floor and upper-floor functions, storeys, conditions etc.

Last updated: 2026-10-23

## Context

Gdynia is a medium-sized city located in the northern Poland. 
Its modernist city centre was
inscribed on the UNESCO World Heritage List on 27 July 2026 as "Gdynia Modernist
City Centre".

Despite this recognition, residents widely perceive problems in the centre:
the mix of ground-floor functions and the lack of new development. These
problems have not been measured. Public sources (OpenStreetMap, official
registers) describe the buildings but not what happens on their ground floors.

## Purpose

To build an accurate, building-level record of the city centre from available
sources, completed by the author, so that the scale and location of these
problems can be measured instead of assumed.

## Scope
- Boundary: UNESCO property plus context additions. #TODO: map of the study area (after plotting, Nov)
- Unit of record: one row = one building, identified by one osm_id or more separated by commas if there are many osm shapes that represent 1 buildings 
- Survey period: 2026-08-01 – 2026-10-22
- Imagery dates: Street View images from 2025-2026 years
- Records (export of 2026-09-30): 1241 rows, 136 empty rows from the export, 1105 after removing them
- Records (export of 2026-10-23): 1038 rows after removing the empty rows, 1417 rows in long table with premises
- Rule for removing rows: OSM tags some minor structures as buildings (external
  stairs, small annexes). They play a negligible role in the analysis, so they
  were left empty during the survey. The cleaning script removes every row with
  an empty ground_floor_function.

## Sources

- OpenStreetMap: skeleton of the dataset, osm_id and addresses. Downloaded 2026-08-01 & 2026-10-22. 
© OpenStreetMap contributors, ODbL
- Google Street View: main source for building characteristics, filled in by hand from the author's assessment
- Field survey: #TODO
- Each row records its source and the author's confidence.






## Data dictionary

| column | meaning | values | source | empty means |
|---|---|---|---|---|
| id | stable record id, never reused | integer | sheet | never empty |
| osm_id | OpenStreetMap building id | text | OSM | never empty |
| addr_street | street name | text | OSM | no street address (see D1) |
| addr_number | house number | text, 3 types eg. 3, 3A, 3-5 | OSM | no house number (see D1) |
| ground_floor_function | ground-floor function(s); several separated by commas | free text, normalised in code | survey | minor OSM structure, row removed in cleaning |
| ground_floor_group | main category of the ground-floor function | from category_map.csv | computed | not computed yet — filled by code, never by hand |
| upper_floor_function | upper-floor function(s) | free text | survey | no upper floors |
| upper_floor_group | main category of upper-floor function | from category_map.csv | computed | not computed yet |
| number_of_storeys | number of storeys | integer | survey | never empty |
| is_mixed_use | mixed use | TODO | computed | not computed yet |
| build_year_est | estimated construction period | TODO: list of allowed values | survey (estimate) | never empty |
| arch_style | architectural style | TODO: list of allowed values | survey | never empty |
| condition | visual condition of the street facade — not a structural assessment | 1 poor: heavy graffiti, falling plaster, visible damage · 2 normal · 3 good: clean, no stains, no visible damage | survey (visual) | never empty |
| max_height | height of the building computed from the point cloud | metres | TODO | not checked yet |
| is_heritage | heritage status | TODO | conservator's list (planned) |not checked yet — does not mean "not a monument" |
| source | source of the record | TODO: list of values | sheet | never empty |
| confidence | confidence that the recorded function is correct | 3 certain: Google Maps label, known place with known function, or the building plainly looks like what it is (e.g. a garage) · 2 likely: function visible on site (e.g. a sign) but not confirmed by a second source · 1 guess: no way to confirm (e.g. closed premises without a sign) | sheet | never empty |
| date_of_checking | date the record was checked | DD.MM.YYYY in the sheet, parsed to a date in code | sheet | never empty |
| number_of_functions | how many premises are located on the ground floor of the building | integer| computed | never empty |


## 4. Decisions

Numbered so code comments can point here (`# see D1`). New decisions go at the bottom; old ones are never deleted — if a decision changes, add a new one that replaces it.

| id | date | decision | reason |
|---|---|---|---|
| D1 | 2026-10-02 | Buildings without a street address keep `addr_street` / `addr_number` empty. | 260 of 292 are garages or technical buildings inside blocks. The rest (incl. 10 residential buildings and harbour-front buildings) have no address in Google Maps. Block interiors are not accessible from the street, so Google Maps is the source for them. |
| D2 | 2026-10-02 | Empty rows from the sheet export are removed in code. | Export artefact (136 rows), not data. |
| D3 | TODO | Period label `Nowożytność` replaced with `Współczesna`. | `Nowożytność` means 16th–18th century. |
| D4 | TODO | Ground-floor functions mapped to main categories with `category_map.csv`. | See section 5. |



## 5. Category mapping

data/reference/category_map.csv maps every ground-floor function recorded in
the survey to a clean name and a main category. It was built from the 292
distinct function values in the raw CSV (export of 2026-10-03), after splitting
multi-function entries, converting to lowercase and trimming spaces (remaining
artefacts such as "_" are described in Known issues). The list was generated in
the notebook 2026.10.04_Excercises; the mapping itself was filled in by hand
and is edited only by hand. Code reads this file and never writes to it.

Columns (separator ;, UTF-8):

| column | meaning |
|---|---|
| functions | function name as recorded in the survey |
| function_clean| unified name: spelling variants and brand names merged |
| category | main category, one of the 16 listed below |
| subcategory | optional finer split within a category; not used yet|

Naming rules for function_clean:
- everything in lowercase; capital letters are added only when plotting
- variants of one function get one name (techniczne, techniczna → techniczna)
- brand names are replaced by the type of premises (żabka → sklep spożywczy)
- shops use the prefix handel (handel ubrania, handel meble)

| category | what belongs here | examples |
|---|---|---|
| transport | public transport facilities | railway station, ticket office |
| organizacje publiczne | public institutions and associations | city administration, schools |
| zdrowie | medical services performed by doctor or medical staff | medical centre, dentist, hospital, optician |
| handel | selling goods taken away by the customer  | grocery, pharmacy, bakery, clothes shop, market |
| usługi | services not covered by a more specific category | hairdresser, beauty salon |
| finanse | financial services | bank, currency exchange, pawn shop |
| gastronomia | food and drink prepared and consumed on site  | restaurant, café, bar, pub, ice-cream parlour |
| noclegi | overnight accommodation | hotel |
| kultura i rozrywka | culture and entertainment | music club, game arcade  |
| biura | office space |office space |
| mieszkaniowa | residential | single-family house, multi-family house|
| garaże | garages |garage |
| przemysł i infrastruktura | industrial, port and storage buildings; technical structures serving housing | warehouse, transformer station, bin shelter |
| kult religijny | religious buildings and their facilities | church, rectory |
| pustostan  | vacant premises | vacant unit |
| brak parteru | buildings or their parts with no ground floor | overhang, elevated connector |

## 6. Processing

- The sheet is for **entering** records only, not for correcting them.
- The raw CSV export (UTF-8) in data/raw/ is never edited by hand.
- All corrections (spelling, merging categories) happen in code, so every change is visible and repeatable.


## 7. Known issues and open questions


- Open question: do Nieużytek,Pustka and Parkingowa count as premises in per-street statistics? Parkingowa and Nieużytek(vacant) yes, Pustka(missing ground floor) no
- funkcja_pietra has 437 empty values — meaning to confirm against liczba_kondygnacji.# DONE
- 292 buildings have no addr_street value. Most are garages and technical buildings inside urban blocks, with no street frontage. They are excluded from all per-street
measures. They stay in the dataset and will be located by geometry (geopandas) later.
-Units: one row of the short table is one building (one osm_id or more separated by commas if there are many osm shapes that represent 1 buildings). One row of the long
table is one premises (building × ground-floor function). number_of_functions is the
number of premises in a building.