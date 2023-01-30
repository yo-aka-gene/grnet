"""
Test for grnet.plot.planetplot
"""
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from grnet.abstract import Estimator
from grnet.clusters import CellClasses
from grnet.dev import typemolds
from grnet.models import PretrainedModel
from grnet.plot import planetplot


@pytest.fixture
def not_subjective():
    return typemolds((pd.core.frame.DataFrame, Estimator, CellClasses))


@pytest.fixture
def not_objective():
    return typemolds(CellClasses)


@pytest.fixture
def not_metric():
    return typemolds(Callable)


@pytest.fixture
def not_ax():
    return typemolds(plt.Axes)


@pytest.fixture
def not_id():
    return typemolds((int, str))


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
def estimators():
    return [
        PretrainedModel(pd.DataFrame(v)) for v in [
            np.ones((5, 5)), np.eye(5), np.tri(5)
        ]
    ]


@pytest.fixture
def names():
    return [
        "a", 0, "b", 1, "c", 2, "d", 3
    ]


@pytest.fixture
def colors():
    return [
        "C0", (.4, .3, .3, .9),
        "r", (.2, .8, .5, .3),
        "k", (.1, .1, .7, .6),
        "b"
    ]


@pytest.fixture
def cellclasses(estimators, names, colors):
    return CellClasses(estimators, names[:3], colors[:3])


@pytest.fixture
def invalid_args(cellclasses):
    return [
        {"subjective": cellclasses, "objective": cellclasses, "id": 123},
        {"subjective": cellclasses, "objective": cellclasses, "id": "asdf"}
    ]


@pytest.fixture
def valid_args(estimators, cellclasses):
    return [
        {
            "subjective": estimators[0].get_matrix(),
            "objective": cellclasses,
            "ax": None,
            "id": None
        },
        {
            "subjective": estimators[0].get_matrix(),
            "objective": cellclasses,
            "ax": None,
            "id": "asdf"
        },
        {
            "subjective": estimators[0].get_matrix(),
            "objective": cellclasses,
            "ax": plt.subplot(),
            "id": "asdf"
        },
        {
            "subjective": estimators[0],
            "objective": cellclasses,
            "ax": None,
            "id": None
        },
        {
            "subjective": estimators[0],
            "objective": cellclasses,
            "ax": None,
            "id": "asdf"
        },
        {
            "subjective": estimators[0],
            "objective": cellclasses,
            "ax": plt.subplot(),
            "id": "asdf"
        },
        {
            "subjective": cellclasses,
            "objective": cellclasses,
            "ax": None,
            "id": "a"
        },
        {
            "subjective": cellclasses,
            "objective": cellclasses,
            "ax": None,
            "id": 2
        },
        {
            "subjective": cellclasses,
            "objective": cellclasses,
            "ax": plt.subplot(),
            "id": "a"
        },
    ]


def test_invalid_dtype_subjective(cellclasses, not_subjective):
    for i, v in enumerate(not_subjective):
        with pytest.raises(AssertionError) as e:
            planetplot(subjective=v, objective=cellclasses)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dtype_objective(cellclasses, not_objective):
    for i, v in enumerate(not_objective):
        with pytest.raises(AssertionError) as e:
            planetplot(subjective=cellclasses, objective=v, id="a")
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dtype_ax(estimators, cellclasses, not_ax):
    for i, v in enumerate(not_ax):
        with pytest.raises(AssertionError) as e:
            planetplot(
                subjective=estimators[0],
                objective=cellclasses,
                ax=v
            )
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dtype_id(cellclasses, not_id):
    for i, v in enumerate(not_id):
        with pytest.raises(AssertionError) as e:
            planetplot(
                subjective=cellclasses,
                objective=cellclasses,
                id=v
            )
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_id_none(estimators, cellclasses):
    for v in estimators:
        planetplot(subjective=v, objective=cellclasses)


def test_id_none_but_data_is_cellclasses(cellclasses):
    with pytest.raises(AssertionError) as e:
        planetplot(subjective=cellclasses, objective=cellclasses)
    assert "None" in f"{e.value}", \
        f"test failed for invalid error mgs: {e.value}"


def test_invalid_df(not_grn, cellclasses):
    for i, v in enumerate(not_grn):
        with pytest.raises(AssertionError) as e:
            planetplot(subjective=v, objective=cellclasses)
        assert "Invalid value" in f"{e.value}", \
            f"test failed for {i}-th input {v}: invalid error msg {e.value}"


def test_invalid_args(invalid_args):
    for i, v in enumerate(invalid_args):
        with pytest.raises(KeyError) as e:
            planetplot(**v)
        assert f"{v['id']}" in f"{e.value}", \
            f"test failed for {i}-th input {v}: invalid error msg {e.value}"


def test_valid_args(valid_args):
    for v in valid_args:
        planetplot(**v)
