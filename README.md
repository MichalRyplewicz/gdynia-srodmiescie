# Gdynia Śródmieście: ground-floor functions analysis

An analysis of buildings and their ground-floor premises in the centre of Gdynia, based on the author's own survey. The project measures how functionally diverse each street is (Shannon entropy of premise categories) and how categories are distributed across streets and building types.

## Data and units

The data comes from two sources:

- **OpenStreetMap building export**: building polygons with `osm_id` and, for many of them, an address.
- **Author's survey** (September–October 2026), based on Google Street View and the author's knowledge of the city: ground- and upper-floor functions, storeys, estimated construction year, architectural style, condition and heritage status.

**Units:**

- **Building**: one row of the short table. Some buildings consist of several OSM polygons; these share an `object_id` and are merged during cleaning. After merging there are **1038 buildings**.
- **Premise**: one row of the long table, i.e. a building × one ground-floor function. Cleaning explodes the ground-floor functions into separate rows, normalises their names and joins the main category (**1417 rows**).

The raw file has 19 columns: `id`, `osm_id`, `object_id`, `addr_street`, `addr_number`, `ground_floor_group`, `ground_floor_function`, `upper_floor_group`, `upper_floor_function`, `number_of_storeys`, `is_mixed_use`, `build_year_est`, `arch_style`, `condition`, `max_height`, `is_heritage`, `source`, `confidence`, `date_of_checking`.

## Key decisions

- **Category map.** Ground-floor functions were cleaned (typos fixed, the same function under one label) and each was assigned one of 16 main categories in `data/reference/category_map.csv`: accommodation, culture and entertainment, finance, garages, gastronomy, health, industry and infrastructure, missing ground floor, office, public organisations, religion, residential, services, trade, transport, vacant.
- **Entropy excludes `vacant` and `missing ground floor`.** Vacancy is reported separately as the vacancy share of a street. Category shares in the heatmaps include both, so they differ slightly from the shares behind the entropy.
- **Natural logarithm** for both the function entropy and the building-type entropy.
- **Street threshold:** only streets with at least 10 premises with a function are included in street metrics (28 streets). The threshold is set in `config.toml`.
- **Buildings without an address are excluded from street metrics.** Many buildings inside city blocks (mostly garages) have no address, so they cannot be linked to a street.

Every decision is explained in more detail in `methodology.md`.

## How to run

```bash
uv sync
uv run nbstripout --install
uv run python -m gdynia_srodmiescie.pipeline
uv run pytest
```

The pipeline goes from the raw CSV to the clean tables in `data/processed/fixed/`, computes building features and street metrics, and saves 6 figures (3 heatmaps and 3 scatter plots) to `figures/`.

Paths, the street threshold and the streets labelled on the scatter plots are set in `config.toml`. Changing them requires no code edits.

## Project structure

```
data/
  raw/               raw survey file
  processed/fixed/   clean short table (buildings) and long table (premises with categories)
  reference/         category map used to assign categories to premises
figures/             figures produced by the pipeline (not tracked by git)
src/gdynia_srodmiescie/
  loading.py            reading CSV files with explicit column types
  cleaning.py           raw file → clean short and long tables
  building_features.py  ground-floor flags, building type, construction period, vacancy kind
  street_metrics.py     street metrics: entropy, vacancy share, ground-floor profile
  styling.py            table styling and figures
  pipeline.py           runs the whole process with one command
tests/               regression tests on a frozen earlier version of the data
config.toml          pipeline settings
methodology.md       detailed methodological decisions
```

The tests use a frozen earlier version of the data (982 buildings) and check that the entropy of Arkadiusza Rybickiego is 1.581 and that 26 streets pass the default threshold.

## Findings

- **The largest street is not the most diverse.** Świętojańska has the most premises (214), but about 80% of them are trade, gastronomy or services. It is a shopping street, not a mixed-use one. The most diverse streets are mid-sized: Armii Krajowej and 3 Maja.
- **Low entropy has two different meanings.** Most streets at the bottom of the ranking have mainly residential ground floors (Generała Józefa Bema, Stefana Żeromskiego, Zgoda, Juliusza Słowackiego). A few are dominated by a single function: industry on Antoniego Hryniewickiego (42%), health on Obrońców Wybrzeża (45%), transport on Plac Konstytucji (35%).
- **Street size and diversity are only weakly related** (Spearman 0.31).
- **Vacancy shares are highest on small streets** (Jana z Kolna 19%), where a few empty premises make a large percentage. On the largest streets the share stays below 8%. Vacancy is not related to diversity (Spearman −0.06).
- **Everyday services sit in mixed-use buildings:** 62.5% of service premises are in residential buildings with ground-floor services, and 92.6% of those buildings were built before 1960.
- **No street contains all categories.** Religion is the rarest: 7 premises on 4 streets.
- **The average relationship between vacancy and diversity is absent** (Spearman −0.06), but the plot is wedge-shaped: the maximum vacancy share tends to fall as diversity rises, and the most diverse streets all have low vacancy. The upper edge is defined by only a few streets, and Jana z Kolna (19% vacancy at mid diversity) is a clear exception.
