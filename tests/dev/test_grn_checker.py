"""
test for functions in grnet.dev.is_grn_matrix
"""
import numpy as np
import pandas as pd
import pytest

from grnet.dev import is_grn_matrix, typemolds


@pytest.fixture
def not_df():
    return typemolds(pd.core.frame.DataFrame)


@pytest.fixture
def not_grn():
    idx1 = [f"a{i}" for i in range(5)]
    col1 = [f"b{i}" for i in range(2)]
    col2 = [f"b{i}" for i in range(5)]
    mtx1, mtx2 = np.random.rand(5, 2), np.random.rand(5, 5)
    diag1, diag2 = np.diag(mtx1), np.diag(mtx2)
    diag1.flags.writeable, diag2.flags.writeable = True, True
    diag1[:], diag2[:] = np.ones(2), np.ones(5)
    return [
        pd.DataFrame(
            np.random.rand(5, 2), index=idx1, columns=col1
        ),
        pd.DataFrame(
            mtx1, index=idx1, columns=col1
        ),
        pd.DataFrame(
            np.ones((5, 2)) - np.eye(5, 2), index=idx1, columns=col1
        ),
        pd.DataFrame(
            np.eye(5, 2), index=idx1, columns=col1
        ),
        pd.DataFrame(
            np.random.rand(5, 2), index=idx1, columns=idx1[:2]
        ),
        pd.DataFrame(
            mtx1, index=idx1, columns=idx1[:2]
        ),
        pd.DataFrame(
            np.ones((5, 2)) - np.eye(5, 2), index=idx1, columns=idx1[:2]
        ),
        pd.DataFrame(
            np.eye(5, 2), index=idx1, columns=idx1[:2]
        ),
        pd.DataFrame(
            np.random.rand(5, 5), index=idx1, columns=col2
        ),
        pd.DataFrame(
            mtx2, index=idx1, columns=col2
        ),
        pd.DataFrame(
            np.ones((5, 5)) - np.eye(5), index=idx1, columns=col2
        ),
        pd.DataFrame(
            np.eye(5), index=idx1, columns=col2
        ),
        pd.DataFrame(
            np.random.rand(5, 5), index=idx1, columns=idx1
        ),
        pd.DataFrame(
            mtx2, index=idx1, columns=idx1
        ),
        pd.DataFrame(
            np.ones((5, 5)) - np.eye(5), index=idx1, columns=idx1
        ),
    ]


@pytest.fixture
def grn_mtx():
    return [
        pd.DataFrame(v) for v in [
            np.ones((5, 5)),
            np.eye(5),
            np.ones((3, 3)),
            np.eye(3),
            np.ones((8, 8)),
            np.eye(8),
        ]
    ]


def test_invalid_dtype(not_df):
    for i, v in enumerate(not_df):
        with pytest.raises(AssertionError) as e:
            is_grn_matrix(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}: got {e.value}"


def test_raise_assertionerror_with_not_grn(not_grn):
    for v in not_grn:
        with pytest.raises(AssertionError):
            is_grn_matrix(v)


def test_correct_return(grn_mtx):
    for i, v in enumerate(grn_mtx):
        assert is_grn_matrix(v) is None, \
            f"test failed for {i}-th input {v}: got {is_grn_matrix(v)}"
