"""
GRN evaluation function d_asterisk
"""

import pandas as pd

from grnet.abstract import Estimator
from grnet.dev import is_grn_matrix, typechecker


def d_asterisk(subjective: Estimator, objective: Estimator) -> float:
    """
    | GRN evaluation function :math:`d^*` is suitable for undirected GRNs generated with PC algorithm.\\
    When :math:`S`: Set of samples, :math:`\\xi:S\\rightarrow S/\\sim` is\
         a clustering function (:math:`\\sim`: equivalent relation), \
            :math:`\\xi(S)(=S/\\sim)`: whole set of equivalent classes induced\
                 by :math:`\\xi`, :math:`F`: a subset of genes,\
                     :math:`^\\forall c, c' \\in S` are arbitrary samples, \
                        and :math:`C_{\\xi(c)}(F), C_{\\xi(c')}(F)` are eigen-cascades of clusters,\
                             :math:`d^* : \\xi(S)\\times\\xi(S)\\rightarrow\\mathbb{R}`\
                                 is given as follows: \\

    .. math::
        d^*(\\xi(c), \\xi(c')) := 1 - \\frac{ |C_{\\xi(c)}(F)\cap C_{\\xi(c')}(F)| }{|C_{\\xi(c)}(F)|}

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

    References
    ----------
    see also our original article for further information
    * original article: https://doi.org/10.1016/j.stemcr.2022.10.015

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from grnet.evaluations import d_asterisk
    >>> from grnet.models import PretrainedModel
    >>> # here we deal undirected GRNs
    >>> names = [f"gene_{i}" for i in range(4)]
    >>> grn1 = pd.DataFrame(np.eye(4), index=names, columns=names)
    >>> grn2 = pd.DataFrame(np.tri(4), index=names, columns=names)
    >>> grn1
            gene_0  gene_1  gene_2  gene_3
    gene_0     1.0     0.0     0.0     0.0
    gene_1     0.0     1.0     0.0     0.0
    gene_2     0.0     0.0     1.0     0.0
    gene_3     0.0     0.0     0.0     1.0
    >>> grn2
            gene_0  gene_1  gene_2  gene_3
    gene_0     1.0     0.0     0.0     0.0
    gene_1     1.0     1.0     0.0     0.0
    gene_2     1.0     1.0     1.0     0.0
    gene_3     1.0     1.0     1.0     1.0
    >>> cluster1, cluster2 = PretrainedModel(data=grn1), PretrainedModel(data=grn2)
    >>> d_asterisk(cluster1, cluster1)
    0.0
    >>> d_asterisk(cluster1, cluster2)
    0.0
    >>> d_asterisk(cluster2, cluster2)
    0.0
    >>> d_asterisk(cluster2, cluster1)
    0.6
    """
    typechecker(subjective, Estimator, "subjective")
    typechecker(objective, Estimator, "objective")
    s_grn = subjective.get_matrix()
    o_grn = objective.get_matrix()
    is_grn_matrix(s_grn)
    is_grn_matrix(o_grn)
    s = s_grn.loc[s_grn.index, s_grn.index]
    o = o_grn.loc[s.index, s.columns]
    return 1 - (((s.values == 1) * (o.values == 1)).sum() / (s.values == 1).sum())
