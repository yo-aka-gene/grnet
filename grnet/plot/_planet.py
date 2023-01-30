"""
function for planet plot
"""
from typing import Callable, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from grnet.abstract import Estimator
from grnet.clusters import CellClasses
from grnet.dev import is_grn_matrix, kwarg_mgr, typechecker
from grnet.evaluations import d_asterisk


def planetplot(
    subjective: Union[pd.core.frame.DataFrame, Estimator, CellClasses],
    objective: CellClasses,
    metric: Callable = d_asterisk,
    ax: plt.Axes = None,
    id: Union[int, str] = None,
    **kwargs
) -> None:
    """
    function for planet plot

    Parameters
    ----------
    subjective: Union[pandas.frame.DataFrame, grnet.abstract.Estimator, grnet.clusters.CellClasses]
        data source for the GRN of the subjective cell class
        (GRN matrix, pretrained Estimator, or CellClasses)

    objective: CellClasses
        data source for the GRNs of the objective cell classes

    metric: Callable, deafult: grnet.evaluations.d_asterisk
        evaluation function for the similarities of cell classes

    ax: matplotlib.pyplot.Axes, default: None
        axes to plot (if `None`, axes will be newly generated)

    id: Union[int, str]
        index or name of the cell class in CellClasses.
        if `subjective` is not a CellClasses, `id` will always be ignored.

    **kwargs
        arguments for plot aethetics

    References
    ----------
    see also our original article for further information on planet plots
    * original article: https://doi.org/10.1016/j.stemcr.2022.10.015
    """
    typechecker(subjective, (pd.core.frame.DataFrame, Estimator, CellClasses), "subjective")
    if isinstance(subjective, pd.core.frame.DataFrame):
        is_grn_matrix(subjective)
        subjective = {
            "grn": subjective,
            "name": kwarg_mgr(kwargs, "name", ""),
            "color": kwarg_mgr(kwargs, "color", "C0")
        }
    elif isinstance(subjective, Estimator):
        subjective = {
            "grn": subjective.get_matrix(),
            "name": kwarg_mgr(kwargs, "name", ""),
            "color": kwarg_mgr(kwargs, "color", "C0")
        }
    else:
        typechecker(id, (int, str), "id")
        subjective = subjective.fetch(id)
    typechecker(objective, CellClasses, "objective")
    objective = [objective.fetch(v) for v in objective.names]
    typechecker(metric, Callable, "metric")

    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    typechecker(ax, plt.Axes, "ax")

    linecolor = kwarg_mgr(kwargs, "linecolor", ".8")
    s = kwarg_mgr(kwargs, "s", 5, (int, float))
    annot_xy_sub = kwarg_mgr(kwargs, "annot_xy_sub", (0, 0), tuple)
    n_dots = kwarg_mgr(kwargs, "n_dots", 1000)
    annot_radius_ob = kwarg_mgr(kwargs, "annot_radius_ob", .01, (float, int))
    annot_xloc_ob = kwarg_mgr(kwargs, "annot_xloc_ob", 0, (float, int))
    annot_yloc_ob = kwarg_mgr(kwargs, "annot_yloc_ob", 0, (float, int))
    zorder = kwarg_mgr(kwargs, "zorder", 0, int)

    ax.scatter(0, 0, color=subjective["color"], s=s)
    ax.annotate(subjective["name"], annot_xy_sub)

    distance = np.array([
        metric(subjective["grn"], ob["grn"]) for ob in objective
    ])

    t = np.linspace(0, 2 * np.pi, num=len(objective) + 2)
    x = np.cos(t)
    y = np.sin(t)
    u = np.linspace(0, 2 * np.pi, num=n_dots)

    for i, d in enumerate(distance):
        ax.scatter(d * x[i + 1], d * y[i + 1], color=objective[i]["color"], s=s)
        ax.annotate(
            objective[i]["name"],
            (d * x[i + 1], d * y[i + 1]),
            (
                (d + annot_radius_ob) * x[i + 1] + annot_xloc_ob,
                (d + annot_radius_ob) * y[i + 1] + annot_yloc_ob
            )
        )
        ax.plot(d * np.cos(u), d * np.sin(u), color=linecolor, zorder=zorder)

    lim = np.abs([*ax.get_xlim()] + [*ax.get_ylim()]).max()
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
