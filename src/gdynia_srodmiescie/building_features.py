import numpy as np
import pandas as pd

NON_SERVICE = [
    "garaże",
    "mieszkaniowa",
    "pustostan",
    "brak parteru",
    "przemysł i infrastruktura",
]


def add_building_floor_flags(df_short, df_long):
    """Function require a short and long version of dataset,
    it returns the short df with four flags: (is_garage, is_residential, is_vacant, is_service),
    based on the categories in the long df
    """
    data_long_features = (
        df_long.assign(
            is_garage=lambda d: d["category"] == "garaże",
            is_residential=lambda d: d["category"] == "mieszkaniowa",
            is_vacant=lambda d: d["category"] == "pustostan",
            is_service=lambda d: ~d["category"].isin(NON_SERVICE),
        )
        .loc[:, ["is_garage", "is_residential", "is_vacant", "is_service"]]
        .groupby("id")
        .any()
    )

    return df_short.join(data_long_features, validate="one_to_one")


def feature_types(d, high_rise):

    return [
        d["number_of_storeys"].ge(high_rise),
        d["is_garage"],
        d["is_service"] & d["upper_floor_function"].str.contains("mieszkaniowa"),
        d["is_service"],
        d["is_residential"] | d["upper_floor_function"].str.contains("mieszkaniowa"),
    ]


FEATURE_TYPES = ["high-rise", "garage", "mixed-use", "service", "residential"]


def add_building_type(df_short, high_rise=10):
    """Function require a short df with 4 floor flags from the add_building_floor_flag function
    and optionally an argument for how many storeys are min. for a skyscrapper.
    it assigns an aditional column with types for each buildings:
    ("high-rise", "garage", "mixed-use", "service", "residential", "other)
    """
    return df_short.assign(
        type=(lambda d: np.select(feature_types(d, high_rise), FEATURE_TYPES, "other"))
    )


PERIOD_BINS = [1800, 1920, 1940, 1960, 1990, 2030]
PERIOD_LABELS = ["before1920", "1920-39", "1940-59", "1960-89", "1990+"]


def add_building_periods(df_short, bins=PERIOD_BINS, labels=PERIOD_LABELS):
    """Function require a short df and adds one aditional column of periods ,
    when the building was build based on the column 'build_year_est'.
    It has optional arguments to change the periods and labels
    """
    return df_short.assign(
        time_period=lambda d: pd.cut(
            d["build_year_est"], bins, right=False, labels=labels
        )
    )


def vacancy_kind_cond(d):

    perc_vacancy = d["vacant"].div(d["sum_premises_per_build"])
    return [perc_vacancy == 0, perc_vacancy == 1.0]


VACANCY_KIND_TYPES = ["without vacant", "full gf vacant"]


def add_vacancy_kind(df_short, df_long):
    """Function require a short df and long df. It returns a short df with another column 'vacacy kind'
    that represent how much share of premises per building are vacant with 3 values: ("without vacant", "full gf vacant", "vacant among working")
    """
    df_long = df_long.loc[lambda d: d["category"] != "brak parteru"]

    return df_short.join(
        pd.crosstab(
            df_long.reset_index()["id"],
            df_long.reset_index()["category"].eq("pustostan"),
        )
        .rename(columns={True: "vacant", False: "active"})
        .assign(sum_premises_per_build=lambda d: d.sum(axis=1))
        .assign(
            vacancy_kind=lambda d: np.select(
                vacancy_kind_cond(d), VACANCY_KIND_TYPES, "vacant among working"
            )
        )
    ).fillna({"vacancy_kind": "without vacant"})
