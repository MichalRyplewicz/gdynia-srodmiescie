def background_gradient(df, cmap="Blues", axis=None, subset=None):
    return df.style.background_gradient(cmap=cmap, axis=axis, subset=subset)


def percent_formatter(styler, subset=None):
    return styler.format(lambda v: "" if v == 0 else f"{v:.1%}", subset=subset)


def decimal_formatter(styler, decimals=2, subset=None):
    return styler.format(lambda v: f"{v:.{decimals}f}", subset=subset)
