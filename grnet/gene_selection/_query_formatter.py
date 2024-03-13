"""
function to format return values of MyGeneInfo().querymany
"""
from typing import Any, List, Union


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
