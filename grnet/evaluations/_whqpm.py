"""
GRN evaluation function Weighted Hamming Quasi-pseudo Metric
"""
import numpy as np
import pandas as pd

from grnet.dev import is_grn_matrix, typechecker


def whqpm(
    subjective: pd.DataFrame,
    objective: pd.DataFrame,
    s_rawdata: pd.DataFrame,
    o_rawdata: pd.DataFrame
) -> float:
    """
    Parameters
    ----------
    subjective: pandas.core.frame.DataFrame
        GRN matrix of the subjective cluster (i.e., cell class)

    objective: pandas.core.frame.DataFrame
        GRN matrix of the objective cluster (i.e., cell class)

    s_rawdata: pandas.DataFrame
        NxD matrix (N: number of samples, D: number of genes) of subjective cell class

    o_rawdata: pandas.DataFrame
        NxD matrix (N: number of samples, D: number of genes) of objective cell class

    Returns
    -------
    Quasi-pseudo distance: float
        quasi-pseudo distance (centering the subjective cluster) between the two clusters
    """
    typechecker(subjective, pd.DataFrame, "subjective")
    typechecker(objective, pd.DataFrame, "objective")
    is_grn_matrix(subjective)
    is_grn_matrix(objective)
    typechecker(s_rawdata, pd.DataFrame, "s_rawdata")
    typechecker(o_rawdata, pd.DataFrame, "o_rawdata")
    s = subjective.loc[subjective.index, subjective.index]
    o = objective.loc[s.index, s.columns]
    s_diag = (s_rawdata.loc[:, s.index] != 0).sum() / s_rawdata.shape[0]
    o_diag = (o_rawdata.loc[:, s.index] != 0).sum() / o_rawdata.shape[0]
    s_other = s.values - np.eye(s.shape[0])
    o_other = o.values - np.eye(o.shape[0])
    n_shared_edges = (s_other.astype(bool) & o_other.astype(bool)).sum()
    return 1 - (n_shared_edges + o_diag.sum()) / (s_other.sum() + s_diag.sum())
