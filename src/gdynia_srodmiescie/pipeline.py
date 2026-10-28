from pathlib import Path

from gdynia_srodmiescie import building_features as bf
from gdynia_srodmiescie import cleaning as cl
from gdynia_srodmiescie import street_metrics as sm
from gdynia_srodmiescie import styling as st
from gdynia_srodmiescie.loading import (
    CATEGORY_COLUMN_TYPES,
    load_df_long,
    load_df_short,
)

RAW_PATH = Path("data/raw/srodmiescie_raw_object_id.csv")
CATEGORY_MAP_PATH = Path("data/reference/category_map.CSV")
PROCESSED_DIR = Path("data/processed/fixed")
FIGURES_DIR = Path("figures")
MIN_FUNCTIONAL = 10


def main():
    ## Loading and cleaning data
    short = load_df_short(RAW_PATH, dayfirst=False)
    category_map = load_df_long(CATEGORY_MAP_PATH, dtype=CATEGORY_COLUMN_TYPES)

    short_fin = short.pipe(cl.clean_short_raw)

    long_fin = short_fin.pipe(cl.long_df_from_short).pipe(
        cl.add_categories, category_map
    )

    short_fin.to_csv(
        "data/processed/fixed/srodmiescie_short.csv", sep=";", encoding="utf-8"
    )

    long_fin.to_csv(
        "data/processed/fixed/srodmiescie_long_categories.csv",
        sep=";",
        encoding="utf-8",
    )

    buildings_features = (
    short_fin.pipe(bf.add_building_floor_flags, long_fin)
    .pipe(bf.add_building_type)
    .pipe(bf.add_building_periods)
    .pipe(bf.add_vacancy_kind, long_fin)
    )

    street_metr = long_fin.pipe(sm.street_metrics, buildings_features,min_functional =  MIN_FUNCTIONAL)






















if __name__ == "__main__":
    main()
