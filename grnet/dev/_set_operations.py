"""
functions to calculate set operations for lists of numpy.ndarray
"""
from typing import List

import numpy as np

from ._checker import typechecker


def multi_union(
    list_of_arr: List[np.ndarray]
) -> np.ndarray:
    """
    function to calculate set-theoretic union for lists of numpy.ndarray

    Parameters
    ----------
    list_of_arr: List[numpy.ndarray]
        list of numpy.ndarray

    Returns
    -------
    union_arr: numpy.ndarray
        numpy.ndarray that has all elements in the set-theoretic union of the arrays

    Examples
    --------
    >>> from grnet.dev import multi_union
    >>> import numpy as np
    >>> x = np.array(["a", "b", "c"])
    >>> y = np.ones(1)
    >>> z = np.array(["foo", "bar"])
    >>> multi_union([x, y, z])
    array(['a', 'b', 'c', '1.0', 'foo', 'bar'], dtype='<U32')
    """
    typechecker(list_of_arr, list, "list_of_arr")
    for i, arr in enumerate(list_of_arr):
        typechecker(arr, np.ndarray, f"list_of_arr[{i}]")
    ret = list_of_arr[0].tolist()
    for arr in list_of_arr[1:]:
        ret += [element for element in arr if element not in ret]
    return np.array(ret)


def multi_intersec(
    list_of_arr: List[np.ndarray]
) -> np.ndarray:
    """
    function to calculate set-theoretic intersection for lists of numpy.ndarray

    Parameters
    ----------
    list_of_arr: List[numpy.ndarray]
        list of numpy.ndarray

    Returns
    -------
    intersec_arr: numpy.ndarray
        numpy.ndarray that has all elements in the set-theoretic intersection of the arrays

    Examples
    --------
    >>> from grnet.dev import multi_intersec
    >>> import numpy as np
    >>> x = np.array(["a", "b", "c"])
    >>> y = np.array(["b", "a", "c"])
    >>> z = np.array(["d", "b", "a"])
    >>> multi_intersec([x, y, z])
    array(['a', 'b'], dtype='<U1')
    """
    typechecker(list_of_arr, list, "list_of_arr")
    for i, arr in enumerate(list_of_arr):
        typechecker(arr, np.ndarray, f"list_of_arr[{i}]")
    ret = list_of_arr[0].tolist()
    for arr in list_of_arr[1:]:
        ret = [element for element in ret if element in arr]
    return np.array(ret)
