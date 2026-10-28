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


def main():
    short = load_df_short(RAW_PATH, dayfirst=False)
    category_map = load_df_long(CATEGORY_MAP_PATH, dtype=CATEGORY_COLUMN_TYPES)

    short_fin = (
        short.pipe(cl.drop_missing, column="ground_floor_function")
        .pipe(
            cl.replace_to_space,
            column="ground_floor_function",
            to_replace="_",
            lower=True,
        )
        .pipe(
            cl.replace_to_space,
            column="upper_floor_function",
            to_replace="_",
            lower=True,
        )
        .pipe(cl.fix_adresses)
        .pipe(cl.fix_styles)
        .pipe(cl.merge_by_same_obj_key)
    )

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


if __name__ == "__main__":
    main()
