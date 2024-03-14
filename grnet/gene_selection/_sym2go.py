"""
functions to summarize GO terms of given gene symbols using set operations
"""
from typing import List

from mygene import MyGeneInfo
import numpy as np

from grnet.dev import (
    multi_union, multi_intersec,
    typechecker
)
from ._query_formatter import fmt_go


def go_union(
    markers: List[str],
    species: str = "human",
    unique: bool = False
) -> np.ndarray:
    """
    function to return GO terms in the set-theoretical union

    Parameters
    ----------
    markers: List[str]
        list of marker gene symbols
    species: str = "human"
        the name of the species (supported in mygene.MyGeneInfo)
    unique: bool = False
        pass True to deal GO terms of the identical GOIDs but in different domains (e.g., "BP", "CC", "MF")
        as the same terms

    Returns
    -------
    union_goterms: numpy.ndarray
        GO terms in the set-theoretical union
    """
    typechecker(markers, list, "markers")
    golist = MyGeneInfo().querymany(
        markers,
        scopes="symbol", fields="go",
        species=species
    )
    return multi_union([
        fmt_go(go_dict=dic, unique=unique) for dic in golist
    ])


def go_intersection(
    markers: List[str],
    species: str = "human",
    unique: bool = False
) -> np.ndarray:
    """
    function to return GO terms in the set-theoretical intersection

    Parameters
    ----------
    markers: List[str]
        list of marker gene symbols
    species: str = "human"
        the name of the species (supported in mygene.MyGeneInfo)
    unique: bool = False
        pass True to deal GO terms of the identical GOIDs but in different domains (e.g., "BP", "CC", "MF")
        as the same terms


    Returns
    -------
    intersec_goterms: numpy.ndarray
        GO terms in the set-theoretical intersection
    """
    typechecker(markers, list, "markers")
    golist = MyGeneInfo().querymany(
        markers,
        scopes="symbol", fields="go",
        species=species
    )
    return multi_intersec([
        fmt_go(go_dict=dic, unique=unique) for dic in golist
    ])
