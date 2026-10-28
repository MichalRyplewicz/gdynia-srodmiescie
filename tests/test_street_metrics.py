from pathlib import Path

import pytest

from gdynia_srodmiescie import building_features as bf
from gdynia_srodmiescie import street_metrics as sm
from gdynia_srodmiescie.loading import load_long, load_short

DATA = Path(__file__).parent / "data"


def test_rybickiego_entropy():
    short = load_short(DATA / "short_old.csv")
    long = load_long(DATA / "long_old.csv")

    buildings = (
        short.pipe(bf.add_building_floor_flags, long)
        .pipe(bf.add_building_type)
        .pipe(bf.add_building_periods)
        .pipe(bf.add_vacancy_kind, long)
    )

    ar_entropy = long.pipe(sm.street_metrics, buildings, min_functional=0).loc[
        "Arkadiusza Rybickiego", "func_entropy"
    ]
    assert ar_entropy == pytest.approx(1.581, abs=0.001)


def test_number_street_metrics():
    short = load_short(DATA / "short_old.csv")
    long = load_long(DATA / "long_old.csv")

    buildings = (
        short.pipe(bf.add_building_floor_flags, long)
        .pipe(bf.add_building_type)
        .pipe(bf.add_building_periods)
        .pipe(bf.add_vacancy_kind, long)
    )

    street_metr = long.pipe(sm.street_metrics, buildings)

    assert len(street_metr) == 26
