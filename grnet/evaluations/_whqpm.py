"""
GRN evaluation function Weighted Hamming Quasi-pseudo Metric
"""
import numpy as np
import pandas as pd

from grnet.dev import is_grn_matrix, typechecker


def whqpm(
    subjective: pd.core.frame.DataFrame,
    objective: pd.core.frame.DataFrame
) -> float:
    """
    Parameters
    ----------
    subjective: pandas.core.frame.DataFrame
        GRN matrix of the subjective cluster (i.e., cell class)

    objective: pandas.core.frame.DataFrame
        GRN matrix of the objective cluster (i.e., cell class)

    Returns
    -------
    Quasi-pseudo distance: float
        quasi-pseudo distance (centering the subjective cluster) between the two clusters
    """
    typechecker(subjective, pd.core.frame.DataFrame, "subjective")
    typechecker(objective, pd.core.frame.DataFrame, "objective")
    is_grn_matrix(subjective)
    is_grn_matrix(objective)
    s = subjective.loc[subjective.index, subjective.index]
    o = objective.loc[s.index, s.columns]
    s_diag = np.diag(s.values)
    o_diag = np.diag(o.values)
    s_other = s.values - s_diag * np.eye(s.shape[0])
    o_other = o.values - o_diag * np.eye(o.shape[0])
    n_shared_edges = (s_other.astype(bool) & o_other.astype(bool)).sum()
    return 1 - (n_shared_edges + o_diag.sum()) / (s_other.sum() + s_diag.sum())
