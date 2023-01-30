"""
function to check if a dict is a cell-class dict
"""
from ._checker import typechecker, valchecker
from ._grn_checker import is_grn_matrix


def is_cellclass_dict(
    dic: dict
) -> None:
    """
    function to check if a dict is a cell-class dict

    Parameters
    ----------
    dic: dict
        a dict to check if it fulfills the requirements for a cell-class dict

    Raises
    ------
    AssertionError
        raised `AssertionError` when dic is not a cell-class dict

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from grnet.dev import is_cellclass_dict as icd
    >>> # general requirements
    >>> # a cell-class dict should include "grn", "name", and "color" in keys
    >>> dict1 = {"grn": pd.DataFrame(np.eye(5)), "name": "a", "color": "C0"}
    >>> icd(dict1)
    >>> # result: pass
    >>> # it is okay to include other keys
    >>> dict2 = {**dict1, "asdf": np.zeros(12), 43: "brahbrah", .4: lambda x: x}
    >>> icd(dict2)
    >>> # result: pass
    >>> # dtypes of values
    >>> # "name" should be str or int, and "color" should be str or Tuple[float] (length should be 4)
    >>> dict3 = {"grn": pd.DataFrame(np.tri(3)), "name": 0, "color": (.8, .7, .6, .9)}
    >>> dict4 = {"grn": pd.DataFrame(np.tri(3)), "name": 0, "color": (.8, "a", 3, np.pi)}
    >>> dict5 = {"grn": pd.DataFrame(np.tri(3)), "name": 0, "color": (.8, .7, .6, .9, .5)}
    >>> icd(dict3)
    >>> # result: pass
    >>> icd(dict4)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid dtype for dic['color'][1]; expected <class 'float'>, got a[<class 'str'>]
    >>> icd(dict5)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. Length of dic['color'] should be 4
    >>> # "grn" should be a GRN matrix
    >>> dict6 = {"grn": 0, "name": "a", "color": "C0"}
    >>> dict7 = {"grn": pd.DataFrame(np.zeros((4, 4))), "name": "a", "color": "C0"}
    >>> icd(dict6)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid dtype for data; expected <class 'pandas.core.frame.DataFrame'>, got 0[<class 'int'>]
    >>> icd(dict7)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. diagonal elements of data sohuld be 1, got      0    1    2    3
    0  0.0  0.0  0.0  0.0
    1  0.0  0.0  0.0  0.0
    2  0.0  0.0  0.0  0.0
    3  0.0  0.0  0.0  0.0
    """
    typechecker(dic, dict, "dic")
    valchecker("grn" in dic, f"'grn' not found in {dic.keys()}")
    valchecker("name" in dic, f"'name' not found in {dic.keys()}")
    valchecker("color" in dic, f"'color' not found in {dic.keys()}")
    is_grn_matrix(dic["grn"])
    typechecker(dic["name"], (str, int), "dic['name']")
    typechecker(dic["color"], (str, tuple), "dic['color']")
    if isinstance(dic["color"], tuple):
        valchecker(
            len(dic["color"]) == 4,
            "Length of dic['color'] should be 4"
        )
        for i, v in enumerate(dic["color"]):
            typechecker(v, float, f"dic['color'][{i}]")
