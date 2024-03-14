"""
function to calculate jaccard index matrix based on GO terms of the given gene symbols
"""
from itertools import product
from typing import List

from mygene import MyGeneInfo
import numpy as np

from grnet.dev import (
    multi_union, multi_intersec,
    typechecker
)
from ._query_formatter import fmt, getid


def go_jaccard_matrix(
    markers: List[str],
    species: str = "human"
) -> np.ndarray:
    """
    function to calculate jaccard index matrix (JIM) based on GO terms of the given gene symbols
    Jaccard Index :math:`J(A,B)` of two sets :math:`A,B` and the element in the :math:`i`-th row \
        and :math:`j`-th column of the JIM is defined as follows:

    .. math::
        J(A, B) := \\frac{A\\cap B}{A \\cup B}

        JIM_{i,j} := J(G_i, G_j)

    where :math:`G_i, G_j` are the sets of GO terms for the :math:`i`-th and :math:`j`-th marker genes.

    Parameters
    ----------
    markers: List[str]
        list of marker gene symbols
    species: str = "human"
        the name of the species (supported in mygene.MyGeneInfo)

    Returns
    -------
    jim: numpy.ndarray
        :math:`n\\times n` JIM where :math:`n` is the number of gene symbols
    """
    typechecker(markers, list, "markers")
    golist = MyGeneInfo().querymany(
        markers,
        scopes="symbol", fields="go",
        species=species
    )
    arr = []
    for (idx1, idx2) in product(
        np.arange(len(markers)),
        np.arange(len(markers))
    ):
        union = multi_union([
            np.unique(
                np.concatenate(
                    [getid(fmt(v)) for v in dic["go"].values()]
                )
            ) for dic in [golist[idx1], golist[idx2]]
        ])
        intersection = multi_intersec([
            np.unique(
                np.concatenate(
                    [getid(fmt(v)) for v in dic["go"].values()]
                )
            ) for dic in [golist[idx1], golist[idx2]]
        ])
        arr += [intersection.size / union.size]
    return np.array(arr).reshape(len(markers), len(markers))
