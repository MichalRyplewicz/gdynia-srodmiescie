# Methodology — Śródmieście building inventory

*Last updated: 2026-10-02*

---

## 1. Purpose and scope

- **Question:** TODO — one sentence: what is this inventory for?
- **Area:** Gdynia, Śródmieście. TODO: boundary (list of streets or a map)
- **Unit of record:** one row = one building, identified by `osm_id`. TODO: confirm
- **Survey period:** 2026-09-27 – 2026-09-30
- **Records:** 1105 (after removing empty rows from the sheet export)

---

## 2. Sources

| source | used for | accessed |
|---|---|---|
| OpenStreetMap | building ids (`osm_id`), addresses (TODO: confirm) | TODO |
| Field survey, from the street | functions, storeys, period, style, condition | 2026-09-27 – 2026-09-30 |
| Google Maps | buildings inside blocks, not accessible from the street | 2026-10-02 |

---

## 3. Data dictionary

An empty cell means different things in different columns. The last column says which.

| column | meaning | values | source | empty means |
|---|---|---|---|---|
| `id` | stable record id, never reused | integer | sheet | never empty |
| `osm_id` | OpenStreetMap building id | integer | OSM | never empty |
| `addr_street` | street name | text | OSM | no street address (see D1) |
| `addr_number` | house number | text, e.g. `12A` | OSM | no house number (see D1) |
| `funkcja_parter` | ground-floor function(s); several separated by commas | free text, normalised in code | survey | never empty |
| `grupa_parter` | main category of the ground-floor function | from `category_map.csv` | computed | not computed yet — filled by code, never by hand |
| `funkcja_pietra` | upper-floor function(s) | free text | survey | TODO: no upper floors, or not checked? |
| `grupa_pietra` | main category of upper-floor function | from `category_map.csv` | computed | not computed yet |
| `liczba_kondygnacji` | number of storeys | integer | survey | never empty |
| `mieszana` | mixed use | TODO | computed | not computed yet |
| `rok_budowy_szac` | estimated construction period | TODO: list of allowed values | survey (estimate) | never empty |
| `styl_arch` | architectural style | TODO: list of allowed values | survey | never empty |
| `stan_tech` | visual condition of the street facade — not a structural assessment | `1` poor: heavy graffiti, falling plaster, visible damage · `2` normal · `3` good: clean, no stains, no visible damage | survey (visual) | never empty |
| `wysokosc_max` | max height allowed by the local plan (MPZP) | metres | MPZP (planned) | not checked yet |
| `zabytek` | heritage status | TODO | conservator's list (planned) | **not checked yet** — does not mean "not a monument" |
| `zrodlo` | source of the record | TODO: list of values | sheet | never empty |
| `pewnosc` | confidence that the recorded function is correct | `3` certain: Google Maps label, known place with known function, or the building plainly looks like what it is (e.g. a garage) · `2` likely: function visible on site (e.g. a sign) but not confirmed by a second source · `1` guess: no way to confirm (e.g. closed premises without a sign) | sheet | never empty |
| `data_sprawdzenia` | date the record was checked | `DD.MM.YYYY` in the sheet, parsed to a date in code | sheet | never empty |

---

## 4. Decisions

Numbered so code comments can point here (`# see D1`). New decisions go at the bottom; old ones are never deleted — if a decision changes, add a new one that replaces it.

| id | date | decision | reason |
|---|---|---|---|
| D1 | 2026-10-02 | Buildings without a street address keep `addr_street` / `addr_number` empty. | 237 of 268 are garages or technical buildings inside blocks. The rest (incl. 7 residential buildings and harbour-front buildings) have no address in Google Maps. Block interiors are not accessible from the street, so Google Maps is the source for them. |
| D2 | 2026-10-02 | Empty rows from the sheet export are removed in code. | Export artefact (136 rows), not data. |
| D3 | TODO | Period label `Nowożytność` replaced with `Współczesna`. | `Nowożytność` means 16th–18th century. |
| D4 | TODO | Ground-floor functions mapped to main categories with `category_map.csv`. | See section 5. |

---

## 5. Category mapping

TODO (from 2026-10-04): how `category_map.csv` was built and how doubtful cases were decided.

---

## 6. Processing

- The sheet is for **entering** records only, not for correcting them.
- The raw CSV export (UTF-8) in `data/raw/` is never edited by hand.
- All corrections (spelling, merging categories) happen in code, so every change is visible and repeatable.

---

## 7. Known issues and open questions

- `funkcja_parter` has inconsistent spelling: `Techniczne` / `Techniczna`, `_` vs space (`Usługi_Szkolenia` / `Handel Odzież`), two prefixes (`Usługi_` / `Usługowa_`). To be normalised in code.
- Open question: do `Nieużytek`, `Pustka` and `Parkingowa` count as premises in per-street statistics?
- `funkcja_pietra` has 437 empty values — meaning to confirm against `liczba_kondygnacji`.
