"""
functions to suggest similar genes based on given gene symbols
"""
from typing import List

from mygene import MyGeneInfo
import numpy as np

from grnet.dev import multi_union, multi_intersec
from ._sym2go import go_intersection
from ._jaccard import go_jaccard_matrix


def sym_by_intersection(
    markers: List[str],
    species: str = "human",
    unique: bool = False
) -> np.ndarray:
    """
    function to suggest similar genes based on the set-theoretical intersection of the GO terms

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
    new_gene_list: numpy.ndarray
        given marker genes + suggested gene symbols
    """
    common_terms = go_intersection(markers, species, unique)
    return multi_intersec([
        np.array([
            hit["symbol"] for hit in MyGeneInfo().query(
                term if unique else term.split("-")[-1],
                scopes="go",
                fields="symbol",
                species=species
            )["hits"]
        ]) for term in common_terms
    ])


def sym_by_union(
    markers: List[str],
    species: str = "human",
    unique: bool = False
) -> np.ndarray:
    """
    function to suggest similar genes based on the set-theoretical union of the GO terms

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
    new_gene_list: numpy.ndarray
        given marker genes + suggested gene symbols
    """
    common_terms = go_intersection(markers, species, unique)
    return multi_union([
        np.array([
            hit["symbol"] for hit in MyGeneInfo().query(
                term if unique else term.split("-")[-1],
                scopes="go",
                fields="symbol",
                species=species
            )["hits"]
        ]) for term in common_terms
    ])


def sym_by_jaccard(
    markers: List[str],
    species: str = "human",
    unique: bool = False
) -> np.ndarray:
    """
    function to suggest similar genes based on the Jaccard Index of the GO terms

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
    new_gene_list: numpy.ndarray
        given marker genes + suggested gene symbols
    """
    extended_list = multi_union([
        np.array(markers),
        sym_by_union(markers, species, unique)
    ]).tolist()
    jim = go_jaccard_matrix(
        extended_list, species, unique
    )
    thresh = go_jaccard_matrix(markers, species, unique).min()
    return np.array(extended_list)[
        np.where(jim[:len(markers), :].min(axis=0) >= thresh)
    ]


def similar_sym(
    markers: List[str],
    species: str = "human",
    unique: bool = False,
    method: str = "jaccard"
) -> np.ndarray:
    """
    wrapper function to suggest similar genes based on the designated method

    Parameters
    ----------
    markers: List[str]
        list of marker gene symbols
    species: str = "human"
        the name of the species (supported in mygene.MyGeneInfo)
    unique: bool = False
        pass True to deal GO terms of the identical GOIDs but in different domains (e.g., "BP", "CC", "MF")
        as the same terms
    method: str = "jaccard"
        choose from "intersection", "jaccard", or "union"

    Returns
    -------
    new_gene_list: numpy.ndarray
        given marker genes + suggested gene symbols
    """
    all_methods = ["intersection", "jaccard", "union"]
    assert method in all_methods, \
        f"Invalid value for method {method}. Choose from {all_methods}"
    return eval(f"sym_by_{method}")(markers, species, unique)
