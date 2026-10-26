import pandas as pd

SHORT_COLUMN_TYPES = {
    "id": "Int64",
    "osm_id": "str",
    "addr_street": "str",
    "addr_number": "str",
    "ground_floor_group": "str",
    "ground_floor_function": "str",
    "upper_floor_group": "str",
    "upper_floor_function": "str",
    "number_of_storeys": "Int64",
    "is_mixed_use": "boolean",
    "build_year_est": "Int64",
    "arch_style": "str",
    "condition": "Int64",
    "max_height": "float64",
    "is_heritage": "str",
    "source": "str",
    "confidence": "Int64",
    "date_of_checking": "str",
    "number_of_functions": "Int64",
}

LONG_COLUMN_TYPES = {"addr_street": "str", "function_clean": "str", "category": "str"}


def load_short(source):
    """Function require a csv file with ';' as separator with id in the first column,
    date of checking is being parsed as date.
    """
    return pd.read_csv(
        source,
        sep=";",
        index_col=0,
        dtype=SHORT_COLUMN_TYPES,
        parse_dates=["date_of_checking"],
    )


def load_long(source):
    """Function require a csv file with ';' as separator with id in the first column,"""
    return pd.read_csv(
        source,
        sep=";",
        index_col=0,
        dtype=LONG_COLUMN_TYPES,
    )
