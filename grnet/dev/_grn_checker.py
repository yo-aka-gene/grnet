"""
functions for checking dataframes if they are GRN matrices
"""
import numpy as np
import pandas as pd

from ._checker import typechecker, valchecker

def is_grn_matrix(
    data: pd.core.frame.DataFrame
) -> None:
    """
    functions for checking dataframes if they are GRN matrices\\

    Parameters
    ----------
    data: pandas.core.frame.DataFrame
        data matrix to be checked if it is a GRN matrix

    Returns
    -------
    None
        it raises `AssertionError` when data is not a GRN matrix

    Notes
    -----
    Definition of GRN matrices are given as follows:
    * DxD matrix (where D is the number of genes, i.e., the number of columns)
    * rows names and columns names are shared
    * all elements are either 0 or 1
    * diagonal elements are 1

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from grnet.dev import is_grn_matrix
    >>> mat_1 = [np.eye(5, 2), 2 * np.eye(2), np.ones((2, 2)) - np.eye(2)]
    >>> invalid_dfs = [pd.DataFrame(v) for v in mat_1]
    >>> is_grn_matrix(np.eye(2))
    Traceback (most recent call last):
        ...
    AssertionError: Invalid dtype for data; expected <class 'pandas.core.frame.DataFrame'>, got [[1. 0.]
     [0. 1.]][<class 'numpy.ndarray'>]
    >>> is_grn_matrix(invalid_dfs[0])
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. data should be a square matrix, got      0    1
    0  1.0  0.0
    1  0.0  1.0
    2  0.0  0.0
    3  0.0  0.0
    4  0.0  0.0
    >>> is_grn_matrix(invalid_dfs[1])
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. all elements in data should be 0 or 1, got      0    1
    0  2.0  0.0
    1  0.0  2.0
    >>> is_grn_matrix(invalid_dfs[2])
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. diagonal elements of data sohuld be 1, got      0    1
    0  0.0  1.0
    1  1.0  0.0
    >>> row_1 = [f"a{i}" for i in range(2)]
    >>> col_1 = [f"b{i}" for i in range(2)]
    >>> invalid_df = pd.DataFrame(np.eye(2), index=row_1, columns=col_1)
    >>> is_grn_matrix(invalid_df)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid value detected. Check the requirements. row names and col names should be the same, got      b0   b1
    a0  1.0  0.0
    a1  0.0  1.0
    >>> valid_df = pd.DataFrame(np.eye(2), index=row_1, columns=row_1)
    >>> is_grn_matrix(valid_df)
    """
    typechecker(data, pd.core.frame.DataFrame, "data")
    valchecker(
        data.index.size == data.columns.size,
        f"data should be a square matrix, got {data}"
    )
    valchecker(
        np.all(data.index == data.columns),
        f"row names and col names should be the same, got {data}"
    )
    valchecker(
        np.all((data == 0) + (data == 1)),
        f"all elements in data should be 0 or 1, got {data}"
    )
    valchecker(
        np.all(np.diag(data) == 1),
        f"diagonal elements of data sohuld be 1, got {data}"
    )
