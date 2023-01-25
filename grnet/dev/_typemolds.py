"""
function to generate type examples for test codes
"""
import numpy as np
import pandas as pd

from typing import List, Tuple, Union
from ._checker import typechecker


def typemolds(
    exception: Union[type, Tuple[type]]
) -> List[type]:
    """
    function to generate type examples for test codes

    Parameters
    ----------
    exception: Union[type, Tuple[type]]
        types to exclude from a list in return

    Returns
    -------
    list_of_types: List[type]
        list of types

    Examples
    --------
    >>> from grnet.dev import typemolds
    >>> not_str = typemolds(str)
    >>> np.all([not isinstance(v, str) for v in not_str])
    True
    >>> not_int = typemolds((int, np.int64))
    >>> np.all([not isinstance(v, (int, np.int64)) for v in not_int])
    True
    """
    if isinstance(exception, tuple):
        for i, v in enumerate(exception):
            typechecker(v, type, f"exception[{i}]")
    else:
        typechecker(exception, type, "exception")
    
    types = [
        "a", 0, 1.1, 1+4j, np.ones(10)[1], np.pi,
        True, type, (), [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]

    return [t for t in types if not isinstance(t, exception)]
