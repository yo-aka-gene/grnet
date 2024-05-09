import anndata as ad
import matplotlib.pyplot as plt
import numpy as np

from grnet.anndata.preprocessing import binarize
from grnet.dev import typechecker


class DORModel:
    def __init__(
        self,
        name: str,
        random_state: int = 0,
        n_trials: int = 100
    ) -> None:
        typechecker(name, str, "name")
        typechecker(random_state, int, "random_state")
        typechecker(n_trials, int, "n_trials")
        self.name = name
        self.seed = random_state
        self.n_trials = n_trials


    def fit(
        self,
        data: ad.AnnData,
        formula: str = None
    ) -> None:
        typechecker(data, ad.AnnData, "data")
        data = binarize(data) if "binarized" not in data.uns else data
        if formula is not None:
            self.formula = formula


    def calibration_plot(
        self,
        ax: plt.Axes = None,
        hide_dots: bool = False,
        hide_curve: bool = False,
        label: str = None,
        linelabel: str = None,
        **kwargs
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        s = kwargs["s"] if "s" in kwargs else .1
        c = kwargs["c"] if "c" in kwargs else ".6"
        lc = kwargs["linecolor"] if "linecolor" in kwargs else "C0"
        ls = kwargs["linestyle"] if "linestyle" in kwargs else None
        ndot = kwargs["ndot"] if "ndot" in kwargs else 1000
        if not hide_dots:
            ax.scatter(self.x, self.y, s=s, c=c, label=label)
        if not hide_curve:
            x = np.linspace(self.x.min(), self.x.max(), ndot)
            ax.plot(x, self.f(x), c=lc, label=linelabel, linestyle=ls)

        ax.set(xlabel="$Mean$", ylabel="$DOR$")
        no_legend_for_scatter = hide_dots or (label is None)
        no_legend_for_curve = hide_curve or (linelabel is None)
        if not (no_legend_for_scatter and no_legend_for_curve):
            ax.legend()
