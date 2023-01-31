"""
GRN plotting function
"""
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from grnet.abstract import Estimator
from grnet.clusters import CellClasses
from grnet.dev import is_grn_matrix, kwarg_mgr, typechecker


def grnplot(
    data: Union[pd.core.frame.DataFrame, Estimator, CellClasses],
    ax: plt.Axes = None,
    id: Union[int, str] = None,
    **kwargs
):
    """
    GRN plotting function

    Parameters
    ----------
    data: Union[pandas.frame.DataFrame, grnet.abstract.Estimator, grnet.clusters.CellClasses]
        data source for plotting GRN (GRN matrix, pretrained Estimator, or CellClasses)

    ax: matplotlib.pyplot.Axes, default: None
        axes to plot the GRN (if `None`, axes will be newly generated)

    id: Union[int, str]
        index or name of the cell class in CellClasses.
        if data is not a CellClasses, `id` will always be ignored.

    **kwargs
        arguments for plot aethetics
    """
    typechecker(data, (pd.core.frame.DataFrame, Estimator, CellClasses), "data")
    if isinstance(data, pd.core.frame.DataFrame):
        is_grn_matrix(data)
        feat = data.columns
        edges = [
            (feat[idx], feat[col]) for idx, col in zip(*np.where(data == 1)) if idx != col
        ]
    elif isinstance(data, Estimator):
        feat = data.data.columns
        edges = data.edges
    else:
        typechecker(id, (int, str), "id")
        data = data.fetch(id)["grn"]
        feat = data.columns
        edges = [
            (feat[idx], feat[col]) for idx, col in zip(*np.where(data == 1)) if idx != col
        ]

    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    typechecker(ax, plt.Axes, "ax")

    feat_dict = {v: i for i, v in enumerate(feat)}
    n = len(feat)

    t = np.linspace(0, 2 * np.pi, num=n + 1)
    x = 10 * np.cos(t)
    y = 10 * np.sin(t)

    color = kwarg_mgr(kwargs, "color", "C0")
    fontsize = kwarg_mgr(kwargs, "fontsize", "x-small")
    edgecolor = kwarg_mgr(kwargs, "edgecolor", color)
    annot_radius = kwarg_mgr(kwargs, "annot_radius", 1.1, (float, int))
    annot_xloc = kwarg_mgr(kwargs, "annot_xloc", -1, (float, int))
    annot_yloc = kwarg_mgr(kwargs, "annot_yloc", -0.4, (float, int))

    ax.scatter(x, y, color=color)

    for i, v in enumerate(feat):
        ax.annotate(
            v,
            (
                annot_radius * x[i] + annot_xloc,
                annot_radius * y[i] + annot_yloc
            ),
            fontsize=fontsize
        )

    for v in edges:
        ax.plot([x[feat_dict[i]] for i in v], [y[feat_dict[i]] for i in v], color=edgecolor)

    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])

    ax.axis("off")
