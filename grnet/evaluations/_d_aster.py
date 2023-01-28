"""
GRN evaluation function d_asterisk
"""
import pandas as pd

from grnet.dev import is_grn_matrix, typechecker

def d_asterisk(
    subjective: pd.core.frame.DataFrame,
    objective: pd.core.frame.DataFrame
) -> float:
    """
    | GRN evaluation function :math:`d^*` is suitable for undirected GRNs generated with PC algorithm.\\
    When :math:`S`: Set of samples, :math:`\\xi:S\\rightarrow S/\\sim` is a clustering function (:math:`\\sim`: equivalent relation), \
        :math:`\\xi(S)(=S/\\sim)`: whole set of equivalent classes induced by :math:`\\xi`, :math:`F`: a subset of genes,\
             :math:`^\\forall c, c' \\in S` are arbitrary samples, and :math:`C_{\\xi(c)}(F), C_{\\xi(c')}(F)` are eigen-cascades of clusters,\
                 :math:`d^* : \\xi(S)\\times\\xi(S)\\rightarrow\\mathbb{R}` is given as follows: \\

    .. math::
        d^*(\\xi(c), \\xi(c')) := 1 - \\frac{ |C_{\\xi(c)}(F)-C_{\\xi(c')}(F)| }{|C_{\\xi(c)}(F)|}

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

    References
    ----------
    see also our original article for further information
    * original article: https://doi.org/10.1016/j.stemcr.2022.10.015

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from grnet.evaluations import d_asterisk
    >>> # here we deal undirected GRNs
    >>> names = [f"gene_{i}" for i in range(4)]
    >>> cluster1 = pd.DataFrame(np.eye(4), index=names, columns=names)
    >>> cluster2 = pd.DataFrame(np.tri(4), index=names, columns=names)
    >>> cluster1
            gene_0  gene_1  gene_2  gene_3
    gene_0     1.0     0.0     0.0     0.0
    gene_1     0.0     1.0     0.0     0.0
    gene_2     0.0     0.0     1.0     0.0
    gene_3     0.0     0.0     0.0     1.0
    >>> cluster2
            gene_0  gene_1  gene_2  gene_3
    gene_0     1.0     0.0     0.0     0.0
    gene_1     1.0     1.0     0.0     0.0
    gene_2     1.0     1.0     1.0     0.0
    gene_3     1.0     1.0     1.0     1.0
    >>> d_asterisk(cluster1, cluster1)
    0.0
    >>> d_asterisk(cluster1, cluster2)
    0.0
    >>> d_asterisk(cluster2, cluster2)
    0.0
    >>> d_asterisk(cluster2, cluster1)
    0.6
    """
    typechecker(subjective, pd.core.frame.DataFrame, "subjective")
    typechecker(objective, pd.core.frame.DataFrame, "objective")
    is_grn_matrix(subjective)
    is_grn_matrix(objective)
    s = subjective.loc[subjective.index, subjective.index]
    o = objective.loc[s.index, s.columns]
    return 1 - (((s.values == 1) * (o.values == 1)).sum() / (s.values == 1).sum())
