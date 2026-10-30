import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def background_gradient(df, cmap="Blues", axis=None, subset=None):
    return df.style.background_gradient(cmap=cmap, axis=axis, subset=subset)


def percent_formatter(styler, subset=None):
    return styler.format(lambda v: "" if v == 0 else f"{v:.1%}", subset=subset)


def decimal_formatter(styler, decimals=2, subset=None):
    return styler.format(lambda v: f"{v:.{decimals}f}", subset=subset)


def plot_heatmap(
    df,
    path,
    figsize=(20, 20),
    labels=True,
    title=None,
    xtick_rotation=90,
    xtick_fontsize=6,
    xtick_ha="center",
):
    fig, ax = plt.subplots(figsize=figsize, dpi=300, layout="constrained")
    g = sns.heatmap(
        df,
        annot=labels,
        cmap="Blues",
        ax=ax,
        mask=df.eq(0),
        fmt="",
        square=True,
        linewidths=2,
        annot_kws={"fontsize": 7},
        cbar_kws={"format": "{x:.0%}", "shrink": 0.5},
    )
    g.set_xticklabels(
        g.get_xticklabels(),
        rotation=xtick_rotation,
        fontsize=xtick_fontsize,
        ha=xtick_ha,
    )

    plt.title(title)
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_scatter(
    df,
    x_name,
    y_name,
    path,
    xscale="linear",
    title="",
    x_label="",
    y_label="",
    label_name=None,
):

    fig, ax = plt.subplots(
        figsize=(6, 4),
        layout="constrained",
    )
    x_column = df[x_name]
    y_column = df[y_name]
    ax.scatter(x=x_column, y=y_column)

    if label_name is not None:
        for street, text in df[label_name].dropna().items():
            ax.annotate(
                text,
                xy=(df.loc[street, x_name], df.loc[street, y_name]),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=8,
            )

    ax.set_title(title)
    ax.set_xlabel(x_label or x_name)
    ax.set_ylabel(y_label or y_name)
    ax.set_xscale(xscale)
    fig.savefig(path, dpi=300)
    plt.close(fig)
