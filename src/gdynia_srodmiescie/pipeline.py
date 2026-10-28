import tomllib
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

CONFIG_PATH = Path("config.toml")


def main():
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    raw_path = Path(config["paths"]["raw_path"])
    category_map_path = Path(config["paths"]["category_map_path"])
    processed_short = Path(config["paths"]["processed_short"])
    processed_long = Path(config["paths"]["processed_long"])
    figures_dir = Path(config["paths"]["figures_dir"])
    min_functional = config["metrics"]["min_functional"]
    streets_to_show = config["figures"]["streets_to_show"]

    figures_dir.mkdir(exist_ok=True)
    ## Loading and cleaning data
    short = load_df_short(raw_path, dayfirst=False)
    category_map = load_df_long(category_map_path, dtype=CATEGORY_COLUMN_TYPES)

    short_fin = short.pipe(cl.clean_short_raw)

    long_fin = short_fin.pipe(cl.long_df_from_short).pipe(
        cl.add_categories, category_map
    )

    short_fin.to_csv(processed_short, sep=";", encoding="utf-8")

    long_fin.to_csv(
        processed_long,
        sep=";",
        encoding="utf-8",
    )

    buildings_features = (
        short_fin.pipe(bf.add_building_floor_flags, long_fin)
        .pipe(bf.add_building_type)
        .pipe(bf.add_building_periods)
        .pipe(bf.add_vacancy_kind, long_fin)
    )

    street_metr = long_fin.pipe(
        sm.street_metrics, buildings_features, min_functional=min_functional
    )

    street_metr = street_metr.assign(
        label=lambda d: d.index.to_series().where(d.index.isin(streets_to_show))
    )

    st.plot_scatter(
        street_metr,
        "num_premises_wo_vacant",
        "func_entropy",
        figures_dir / "num_prem_func_entropy.png",
        xscale="log",
        label_name="label",
    )
    st.plot_scatter(
        street_metr,
        "num_premises_wo_vacant",
        "share_vacant",
        figures_dir / "num_prem_share_vacant.png",
        xscale="log",
        label_name="label",
    )
    st.plot_scatter(
        street_metr,
        "func_entropy",
        "share_vacant",
        figures_dir / "func_entropy_share_vacant.png",
        xscale="log",
        label_name="label",
    )


if __name__ == "__main__":
    main()
