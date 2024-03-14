"""
function to format return values of MyGeneInfo().querymany
"""
from typing import Any, Dict, List, Union


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
