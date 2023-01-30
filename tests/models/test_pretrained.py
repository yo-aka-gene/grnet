"""
Test for PretrainedModel class
"""
import numpy as np
import pandas as pd
import pytest

from grnet.dev import typemolds
from grnet.models import PretrainedModel


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


def test_init_invalid_dtype(not_df):
    for i, v in enumerate(not_df):
        with pytest.raises(AssertionError) as e:
            PretrainedModel(data=v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_init_not_grn_matrix(not_grn):
    for i, v in enumerate(not_grn):
        with pytest.raises(AssertionError) as e:
            PretrainedModel(data=v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_init_correct_data(grn_mtx):
    for i, v in enumerate(grn_mtx):
        model = PretrainedModel(data=v)
        assert np.all(model.data == v), \
            f"test failed for {i}-th input: expected {v}, got {model.data}"


def test_init_correct_edges(grn_mtx):
    for i, v in enumerate(grn_mtx):
        model = PretrainedModel(data=v)
        feat = v.columns
        expect = [
            (feat[idx], feat[col]) for idx, col in zip(*np.where(v == 1)) if idx != col
        ]
        assert model.edges == expect, \
            f"test failed for {i}-th input: expected {expect}, got {model.edges}"
