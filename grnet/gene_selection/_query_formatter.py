"""
function to format return values of MyGeneInfo().querymany
"""
from typing import Any, Dict, List, Union

import numpy as np


def fmt(x: Union[Any, list]) -> Union[List[Any], list]:
    """
    function to format return values of MyGeneInfo().querymany

    Parameters
    ----------
    x: Union[Any, list]
        return value of MyGeneInfo().querymany

    Returns
    -------
    x_list: Union[List[Any], list]
        returns x if x is a list; otherwise [x]

    Examples
    --------
    >>> from grnet.gene_selection._query_formatter import fmt
    >>> fmt(["a", "b", "c"])
    ['a', 'b', 'c']
    >>> fmt("d")
    ['d']
    """
    return x if isinstance(x, list) else [x]


def getid(lst: List[Dict[str, Any]]) -> List[str]:
    """
    function to get 'id' terms from return values of MyGeneInfo().querymany

    Parameters
    ----------
    lst: List[Dict[str, Any]]
        return value of MyGeneInfo().querymany

    Returns
    -------
    id_list: List[str]
        list of go ids

    Examples
    --------
    >>> from grnet.gene_selection._query_formatter import getid
    >>> getid([{"id": f"GO:xxxxxx{i}"} for i in range(3)])
    ['GO:xxxxxx0', 'GO:xxxxxx1', 'GO:xxxxxx2']
    """
    return [v["id"] for v in lst]


def fmt_go(
    go_dict: Dict[str, Union[Any, list]],
    unique: bool = False
) -> np.ndarray:
    """
    function to return 'id' terms from return values of MyGeneInfo().querymany as numpy.ndarray

    Parameters
    ----------
    go_dict: Dict[str, Union[Any, list]]
        return dictionary of MyGeneInfo().querymany (which returns a list of dicts)
    unique: bool = False
        pass True to deal GO terms of the identical GOIDs but in different domains (e.g., "BP", "CC", "MF")
        as the same terms

    Returns
    -------
    arr: numpy.ndarray
        numpy array of GOIDs [str] if unique == True; otherwise, numpy array of dict
    """
    return np.unique(
        np.concatenate(
            [getid(fmt(v)) for v in go_dict["go"].values()]
        )
    ) if unique else np.concatenate(
        [fmt(v) for v in go_dict["go"].values()]
    )
