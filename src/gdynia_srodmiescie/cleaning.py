import numpy as np
import pandas as pd


def drop_missing(df, column):
    """Removes the rows that contains Na data in inputted column

    Requires a dataframe and column
    """
    return df.dropna(subset=f"{column}")


def replace_to_space(df, column, to_replace, lower=False):
    """Replaced the selected symbol to space in chosen column, optionally lowers the elements

    Requires a dataframe, a column and an element to replace, optionally a bool whether to lower the elements of the column
    """
    replaced = df.assign(**{column: lambda d: d[column].str.replace(to_replace, " ")})

    if lower:
        replaced = replaced.assign(**{column: lambda d: d[column].str.lower()})

    return replaced


STREET_FIXES = {
    "Hryniewickiego": "Antoniego Hryniewickiego",
    "Wendy": "Tadeusza Wendy",
    "Plac Kaszubski - Jana z Kolna": "Jana z Kolna",
}


def fix_adresses(df, fixes=STREET_FIXES):
    """Fixes the typos in the street names and correxts the adress numbers by removing spaces and uppers them

    Requires a short dataframe and a dictionary with the fixes listed
    """
    return df.assign(
        addr_street=lambda d: d["addr_street"].replace(fixes),
        addr_number=lambda d: d["addr_number"].str.strip().str.upper(),
    )


STYLE_FIXES = {
    "nowożytnośc": "współczesność",
    "współczsnośc": "współczesność",
    "wspóółczesność": "współczesność",
    "wspóczesność": "współczesność",
    "współczesnosc": "współczesność",
    "traycjonalizm": "tradycjonalizm",
    "wiejski": "tradycjonalizm",
    "art. deco": "modernizm",
    "artdeco": "modernizm",
    "wertykalizm": "modernizm",
    "nowożytność": "współczesność",
}


def fix_styles(df, fixes=STYLE_FIXES):
    """Fixes the typos in the style names

    Requites a short dataframe and a dictionary with the fixes listed
    """
    return df.assign(
        arch_style=lambda d: d["arch_style"].str.lower().str.strip().replace(fixes),
    )


def connect_func(s):
    func = s.str.split(",").explode().str.strip().str.lower().dropna().unique()
    return ",".join(func) if len(func) > 0 else pd.NA


def merge_by_same_obj_key(df):
    """Connects the rows of elements with the same object_id

    Requires a short dataframe
    """

    with_obj_id = (
        df.loc[df["object_id"].notna()]
        .reset_index()
        .sort_values(
            ["number_of_storeys", "osm_id", "ground_floor_function"], ascending=False
        )
        .groupby("object_id", sort=False)
        .agg(
            id=("id", "min"),
            osm_id=("osm_id", ",".join),
            addr_street=("addr_street", "first"),
            addr_number=("addr_number", "first"),
            ground_floor_group=("ground_floor_group", "first"),
            ground_floor_function=("ground_floor_function", connect_func),
            upper_floor_group=("upper_floor_group", "first"),
            upper_floor_function=("upper_floor_function", "first"),
            number_of_storeys=("number_of_storeys", "max"),
            is_mixed_use=("is_mixed_use", "max"),
            build_year_est=("build_year_est", "first"),
            arch_style=("arch_style", "first"),
            condition=("condition", "first"),
            max_height=("max_height", "max"),
            is_heritage=("is_heritage", "first"),
            source=("source", "first"),
            confidence=("confidence", "min"),
            date_of_checking=("date_of_checking", "max"),
        )
        .reset_index(drop=True)
    )

    without_obj_id = df.loc[df["object_id"].isna()].reset_index()[with_obj_id.columns]

    return pd.concat([with_obj_id, without_obj_id]).set_index("id").sort_index()


def long_df_from_short(df):
    """Returns a long df from a short one, based on the column and the lists in'ground floor function'

    Requires a short dataframe
    """
    return (
        df.assign(
            ground_floor_function=lambda d: d["ground_floor_function"].str.split(",")
        )
        .explode("ground_floor_function")
        .assign(ground_floor_function=lambda d: d["ground_floor_function"].str.strip())
        .loc[:, ["addr_street", "ground_floor_function"]]
    )


def add_categories(long, category_map):
    """Adds category column to the long df based on the function and correct the function

    Requires a long dataframe and a category map
    """
    long_category = pd.merge(
        long,
        category_map,
        left_on="ground_floor_function",
        right_index=True,
        how="left",
        validate="many_to_one",
    )

    missing = long_category.loc[
        long_category["category"].isna(), "ground_floor_function"
    ].unique()
    assert len(missing) == 0, f"functions without category: {list(missing)}"

    return long_category.loc[:, ["addr_street", "function_clean", "category"]]


def clean_short_raw(df):
    """Returns a cleaned short df, correcting typos in styles and adresses, merged by object id

    Requires short dataframe
    """
    return (
        df.pipe(drop_missing, column="ground_floor_function")
        .pipe(
            replace_to_space,
            column="ground_floor_function",
            to_replace="_",
            lower=True,
        )
        .pipe(
            replace_to_space,
            column="upper_floor_function",
            to_replace="_",
            lower=True,
        )
        .pipe(fix_adresses)
        .pipe(fix_styles)
        .pipe(merge_by_same_obj_key)
    )
