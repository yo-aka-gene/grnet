"""
GRN evaluation function Weighted Hamming Quasi-pseudo Metric
"""

import numpy as np
import pandas as pd

from grnet.abstract import Estimator
from grnet.dev import is_grn_matrix, typechecker


def whqpm(subjective: Estimator, objective: Estimator) -> float:
    """
    Parameters
    ----------
    subjective: Estimator
        GRNet model of the subjective cluster (i.e., cell class)

    objective: Estimator
        GRNet model of the objective cluster (i.e., cell class)

    Returns
    -------
    Quasi-pseudo distance: float
        quasi-pseudo distance (centering the subjective cluster) between the two clusters
    """
    typechecker(subjective, Estimator, "subjective")
    typechecker(objective, Estimator, "objective")
    s_grn = subjective.get_matrix()
    s_rawdata = subjective.data
    o_grn = objective.get_matrix()
    o_rawdata = objective.data
    is_grn_matrix(s_grn)
    is_grn_matrix(o_grn)
    s = s_grn.loc[s_grn.index, s_grn.index]
    o = o_grn.loc[s.index, s.columns]
    s_diag = (s_rawdata.loc[:, s.index] != 0).sum() / s_rawdata.shape[0]
    o_diag = (o_rawdata.loc[:, s.index] != 0).sum() / o_rawdata.shape[0]
    diag_min = pd.concat([s_diag, o_diag], axis=1).min(axis=1)
    s_other = s.values - np.eye(s.shape[0])
    o_other = o.values - np.eye(o.shape[0])
    n_shared_edges = (s_other.astype(bool) & o_other.astype(bool)).sum()
    return 1 - (n_shared_edges + diag_min.sum()) / (s_other.sum() + s_diag.sum())
