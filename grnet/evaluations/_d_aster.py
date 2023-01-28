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
    | GRN evaluation function :math:`d^*` \\
    when :math:`S`: Set of samples, :math:`\\xi:S\\rightarrow S/\\sim` is a clustering function (:math:`\\sim`: equivalent relation), \
        :math:`\\xi(S)(=S/\\sim)`: whole set of equivalent classes induced by :math:`\\xi`, :math:`F`: a subset of genes,\
             :math:`^\\forall c, c' \\in S` are arbitrary samples, and :math:`C_{\\xi(c)}(F), C_{\\xi(c')}(F)` are eigen-cascades of clusters,\
                 :math:`d^* : \\xi(S)\\times\\xi(S)\\rightarrow\\mathbb{R}` is given as follows: \\

    .. math::
        d^*(\\xi(c), \\xi(c')) := 1 - \\frac{ |C_{\\xi(c)}(F)-C_{\\xi(c')}(F)| }{|C_{\\xi(c)}(F)|}

    References
    ----------
    see also our original article for further information
    * original article: https://doi.org/10.1016/j.stemcr.2022.10.015
    """
    typechecker(subjective, pd.core.frame.DataFrame, "subjective")
    typechecker(objective, pd.core.frame.DataFrame, "objective")
    is_grn_matrix(subjective)
    is_grn_matrix(objective)
    s = subjective.loc[subjective.index, subjective.index]
    o = objective.loc[s.index, s.columns]
    return 1 - (((s.values == 1) * (o.values == 1)).sum() / (s.values == 1).sum())
