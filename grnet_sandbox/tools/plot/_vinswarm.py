from typing import Any, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def vinswarm(
    data: pd.DataFrame,
    x: Any = None,
    y: Any = None,
    hue: Any = None,
    inner: Any = None,
    cut: Union[int, float] = 0,
    alpha: Union[int, float] = .5,
    s: Union[int, float] = 1,
    jitter: Union[int, float] = .4,
    zorder: int = 0,
    ax: plt.Axes = None,
    **kwargs
) -> None:
    if ax is None:
        _, ax = plt.subplots()

    sns.violinplot(
        data=data,
        x=x, y=y, hue=hue,
        inner=inner, cut=cut,
        alpha=alpha,
        **kwargs
    )
    sns.stripplot(
        data=data,
        x=x, y=y, hue=hue,
        s=s,
        jitter=jitter,
        zorder=zorder,
        **kwargs
    )
