import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def background_gradient(df, cmap="Blues", axis=None, subset=None):
    return df.style.background_gradient(cmap=cmap, axis=axis, subset=subset)


def percent_formatter(styler, subset=None):
    return styler.format(lambda v: "" if v == 0 else f"{v:.1%}", subset=subset)


def decimal_formatter(styler, decimals=2, subset=None):
    return styler.format(lambda v: f"{v:.{decimals}f}", subset=subset)


def plot_heatmap(
    cross_table,
    path,
    title="",
    cmap="Blues",
    fmt="{:.0%}",
    other_fmt="{:g}",
    subset=None,
    x_label="",
    y_label="",
    rotation_xticks=0,
):
    """This function saves a crosstab as a heatmap with numbers in each cell"""
    if subset is None:
        subset = list(cross_table.columns)
    colored = cross_table[subset].reindex(columns=cross_table.columns)

    fig, ax = plt.subplots(
        figsize=(cross_table.shape[1] + 1, cross_table.shape[0] + 1),
        layout="constrained",
    )
    im = ax.imshow(colored, cmap=cmap, aspect="auto")

    ha = "right" if rotation_xticks else "center"
    ax.set_xticks(
        range(cross_table.shape[1]),
        labels=cross_table.columns,
        rotation=rotation_xticks,
        ha=ha,
        rotation_mode="anchor",
    )
    ax.set_yticks(range(cross_table.shape[0]), labels=cross_table.index)

    middle = (colored.max().max() + colored.min().min()) / 2
    for i in range(cross_table.shape[0]):
        for j in range(cross_table.shape[1]):
            value = cross_table.iat[i, j]
            if cross_table.columns[j] in subset:
                if value == 0:
                    continue
                text = fmt.format(value)
                color = "white" if value > middle else "black"
            else:
                text = other_fmt.format(value)
                color = "black"
            ax.text(j, i, text, ha="center", va="center", color=color)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.colorbar(im, ax=ax, format=FuncFormatter(lambda x, _: fmt.format(x)))
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
