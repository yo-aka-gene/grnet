"""
Utility functions for figures
"""
from typing import Any, Tuple, Union

from ._checker import typechecker


def kwarg_mgr(
    kwargs: dict,
    key: str,
    default: Any,
    typehint: Union[type, Tuple[type]] = None
) -> Any:
    """
    function to manage kwargs in functions

    Parameters
    ----------
    kwargs: dict
        dictionary of arguments

    key: str
        key name of the argument

    default: Any
        default value for the argument

    typehint: Union[type, Tuple[type]], default: None
        if not `None`, `grnet.dev.typechecker` wll be run for `kwargs[key]`

    Returns
    -------
    assigned value: Any
        `kwargs[key]` if `key` in `kwargs`; otherwise, `default`

    Examples
    --------
    >>> from grnet.dev import kwarg_mgr
    >>> dict1 = {"a": 0, "b": 1}
    >>> kwarg_mgr(kwargs=dict1, key="a", default=2)
    0
    >>> kwarg_mgr(kwargs=dict1, key="b", default="asdf")
    1
    >>> kwarg_mgr(kwargs=dict1, key="c", default="asdf")
    'asdf'
    >>> kwarg_mgr(kwargs=dict1, key="b", default="asdf", typehint=int)
    1
    >>> kwarg_mgr(kwargs=dict1, key="b", default="asdf", typehint=str)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid dtype for kwargs[b]; expected <class 'str'>, got 1[<class 'int'>]
    >>> kwarg_mgr(kwargs=dict1, key="c", default=None, typehint=str)
    """
    typechecker(kwargs, dict, "kwargs")
    typechecker(key, str, "key")
    ret = default
    if key in kwargs:
        ret = kwargs[key]
        if typehint is not None:
            typechecker(typehint, (type, tuple), "typehint")
            if isinstance(typehint, tuple):
                for i, v in enumerate(typehint):
                    typechecker(v, type, f"typehint[{i}]")
            typechecker(ret, typehint, f"kwargs[{key}]")
    return ret
