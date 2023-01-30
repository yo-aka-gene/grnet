"""
Test for is_cellclass_dict
"""
import numpy as np
import pandas as pd
import pytest

from grnet.dev import is_cellclass_dict, typemolds


@pytest.fixture
def not_dict():
    return typemolds(dict)


@pytest.fixture
def invalid_dict():
    grn = {"grn": pd.DataFrame(np.eye(3))}
    name = {"name": "cluster_1"}
    color = {"color": (.5, .5, .5, .5)}
    return [
        {},
        {"a": 0, "b": 0, "c": 0},
        grn,
        name,
        color,
        {**grn, **name},
        {**grn, **color},
        {**name, **color}  
    ]


@pytest.fixture
def not_df_for_grn():
    const = {"name": "cluster_1", "color": (.5, .5, .5, .5)}
    return [
        {**const, "grn": v} for v in typemolds(pd.core.frame.DataFrame)  
    ]


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
def not_grn_for_grn(not_grn):
    const = {"name": "cluster_1", "color": (.5, .5, .5, .5)}
    return [
        {**const, "grn": v}  for v in not_grn
    ]


@pytest.fixture
def correct_dict():
    return [
        {"grn": pd.DataFrame(np.eye(5)), "name": "a", "color": "C0"},
        {"grn": pd.DataFrame(np.eye(5)), "name": "a", "color": "C0", "asdf": np.zeros(12)},
        {"grn": pd.DataFrame(np.tri(3)), "name": 0, "color": (.8, .7, .6, .9)},
        {"name": "a", "color": "C0", "grn": pd.DataFrame(np.eye(5))},
    ]


def test_invalid_dtype(not_dict):
    for i, v in enumerate(not_dict):
        with pytest.raises(AssertionError) as e:
            is_cellclass_dict(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dict(invalid_dict):
    for i, v in enumerate(invalid_dict):
        with pytest.raises(AssertionError) as e:
            is_cellclass_dict(v)
        assert f"{v.keys()}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_not_df_for_grn(not_df_for_grn):
    for i, v in enumerate(not_df_for_grn):
        with pytest.raises(AssertionError) as e:
            is_cellclass_dict(v)
        assert f"{v['grn']}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_not_grn_for_grn(not_grn_for_grn):
    for i, v in enumerate(not_grn_for_grn):
        with pytest.raises(AssertionError) as e:
            is_cellclass_dict(v)
        assert "Invalid" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_correct_dict(correct_dict):
    for i, v in enumerate(correct_dict):
        assert is_cellclass_dict(v) is None, \
            f"test failed for {i}-th input {v}"
