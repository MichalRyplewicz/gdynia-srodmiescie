import numpy as np
import pandas as pd


def street_metrics(
    df_long, df_short=None, min_functional=10, cat_omitted=("brak parteru", "pustostan")
):

    streets_long = pd.concat(
        [
            df_long.loc[lambda d: d["category"] != "brak parteru"]
            .assign(is_vacant=lambda d: d["category"] == "pustostan")
            .groupby("addr_street")
            .agg(num_premises=("category", "size"), num_vacant=("is_vacant", "sum"))
            .assign(
                num_premises_wo_vacant=lambda d: d["num_premises"] - d["num_vacant"],
                share_vacant=lambda d: d["num_vacant"].div(d["num_premises"]),
            ),
            df_long.loc[lambda d: ~d["category"].isin(cat_omitted)]
            .groupby("addr_street")["category"]
            .value_counts()
            .to_frame("premise_per_cat")
            .assign(
                total_premises_per_street=lambda d: d.groupby("addr_street")[
                    "premise_per_cat"
                ].transform("sum"),
                share=lambda d: d["premise_per_cat"].div(
                    d["total_premises_per_street"]
                ),
                lnshare_mult_share=lambda d: np.log(d["share"]).mul(d["share"]).mul(-1),
            )
            .groupby("addr_street")
            .agg(
                num_cat=("premise_per_cat", lambda s: s.gt(0).sum()),
                leader_share=("share", "max"),
                func_entropy=("lnshare_mult_share", "sum"),
            )
            .assign(eff_cat=lambda d: np.exp(d["func_entropy"])),
        ],
        axis=1,
    ).loc[
        :,
        [
            "num_premises",
            "num_premises_wo_vacant",
            "num_vacant",
            "share_vacant",
            "leader_share",
            "func_entropy",
            "num_cat",
            "eff_cat",
        ],
    ]
    if df_short is not None:
        streets_long = streets_long.join(
            df_short.groupby("addr_street")
            .agg(
                num_buildings=("osm_id", "size"),
                num_mix_use=("type", lambda d: (d == "mixed-use").sum()),
            )
            .assign(share_mix_use=lambda d: d["num_mix_use"].div(d["num_buildings"]))
        )
    return streets_long.loc[lambda d: d["num_premises_wo_vacant"].ge(min_functional)]


def ground_floor_profile(df_long, df_short, types=("mixed-use", "service")):

    premises_wth_types = df_long.join(df_short.loc[:, "type"], validate="many_to_one")

    return (
        pd.crosstab(
            index=premises_wth_types.reset_index()["category"],
            columns=premises_wth_types.reset_index().loc[
                lambda d: d["type"].isin(types), "type"
            ],
            normalize="columns",
        )
        .assign(
            div_1_2=lambda d: d.loc[:, types[0]].div(d.loc[:, types[1]]),
            sum_build_types=pd.crosstab(
                index=premises_wth_types.reset_index()["category"],
                columns=premises_wth_types.reset_index().loc[
                    lambda d: d["type"].isin(types), "type"
                ],
            ).sum(axis=1),
            is_sum_ge_10=lambda d: d["sum_build_types"].ge(10),
        )
        .sort_values("div_1_2", ascending=False)
    )


def building_type_shares(df_short):

    return pd.crosstab(
        index=df_short.reset_index()["addr_street"],
        columns=df_short.reset_index()["type"],
        normalize="index",
    )


def entropy_from_shares(df_share, column_name="type"):
    df_share = df_share.replace(0, np.nan)
    return (
        (np.log(df_share) * df_share)
        .sum(axis=1)
        .mul(-1)
        .to_frame(name=f"{column_name}_entropy")
        .assign(
            **{
                f"effective_{column_name}": lambda d: np.exp(
                    d[f"{column_name}_entropy"]
                )
            }
        )
    )
