"""
test for grnet.evaluations.d_asterisk
"""
import numpy as np
import pandas as pd
import pytest

from grnet.dev import typemolds
from grnet.evaluations import d_asterisk


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
            np.tri(5),
            np.ones((3, 3)),
            np.eye(3),
            np.tri(3),
            np.ones((8, 8)),
            np.eye(8),
            np.tri(8),
        ]
    ]


def test_invalid_dtype_subjective(not_df):
    df = pd.DataFrame(np.eye(5))
    for i, v in enumerate(not_df):
        with pytest.raises(AssertionError) as e:
            d_asterisk(v, df)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}: got {e.value}"


def test_invalid_dtype_objective(not_df):
    df = pd.DataFrame(np.eye(5))
    for i, v in enumerate(not_df):
        with pytest.raises(AssertionError) as e:
            d_asterisk(df, v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}: got {e.value}"


def test_raise_assertionerror_with_not_grn_subjective(not_grn):
    df = pd.DataFrame(np.eye(5))
    for v in not_grn:
        with pytest.raises(AssertionError):
            d_asterisk(v, df)


def test_raise_assertionerror_with_not_grn_objective(not_grn):
    df = pd.DataFrame(np.eye(5))
    for v in not_grn:
        with pytest.raises(AssertionError):
            d_asterisk(df, v)


def test_reflexive(grn_mtx):
    for i, v in enumerate(grn_mtx):
        assert d_asterisk(v, v) == 0, \
            f"test failed for {i}-th input {v}: got {d_asterisk(v)}"


def test_ones_objective(grn_mtx):
    for i, v in enumerate(grn_mtx):
        ob = pd.DataFrame(np.ones(v.shape))
        assert d_asterisk(v, ob) == 0, \
            f"test failed for {i}-th input {v}: got {d_asterisk(v, ob)}"


def test_ones_subjective(grn_mtx):
    for i, v in enumerate(grn_mtx):
        sub = pd.DataFrame(np.ones(v.shape))
        expect = 1 - (sub.values * v.values).sum() / sub.values.sum()
        assert d_asterisk(sub, v) == expect, \
            f"test failed for {i}-th input {v}: expected {expect}, got {d_asterisk(sub, v)}"
