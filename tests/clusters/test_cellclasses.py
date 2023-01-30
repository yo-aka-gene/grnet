"""
Test for grnet.clusters.CellClasses
"""
import numpy as np
import pandas as pd
import pytest

from grnet.abstract import Estimator
from grnet.clusters import CellClasses
from grnet.dev import is_cellclass_dict, is_grn_matrix, typemolds
from grnet.models import PretrainedModel


@pytest.fixture
def not_list():
    return typemolds(list)


@pytest.fixture
def estimators():
    return [
        PretrainedModel(pd.DataFrame(v)) for v in [
            np.ones((5, 5)), np.eye(4), np.tri(7)
        ]
    ]


@pytest.fixture
def not_list_of_estimators(estimators):
    return [
        [*estimators, v] for v in typemolds(Estimator)
    ]


@pytest.fixture
def not_list_of_names():
    return [
        ["cluster1", 123, v] for v in typemolds((str, int))
    ]


@pytest.fixture
def not_color():
    return typemolds((str, list))


@pytest.fixture
def not_list_of_colors():
    return [
        ["C0", (.1, .5, .3, .2), v] for v in typemolds((str, tuple))
    ]


@pytest.fixture
def not_tuple_of_colors():
    return [
        [(.1, .5, .3, .2), (.2, .3, .4, v)] for v in typemolds(float)
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
def inconsistent_length(estimators, names, colors):
    return [
        {"models": estimators, "names": names, "colors": colors},
        {"models": estimators, "names": names[:3], "colors": colors},
        {"models": estimators, "names": names, "colors": colors[:3]},
        {"models": estimators, "names": names[:7], "colors": colors}
    ]


@pytest.fixture
def not_id():
    return typemolds((int, str))


def test_invalid_dtype_models(not_list):
    for i, v in enumerate(not_list):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_element_dtype_models(not_list_of_estimators):
    for i, v in enumerate(not_list_of_estimators):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dtype_names(estimators, not_list):
    for i, v in enumerate(not_list):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=estimators, names=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_element_dtype_names(estimators, not_list_of_names):
    for i, v in enumerate(not_list_of_names):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=estimators, names=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_dtype_colors(estimators, not_color):
    for i, v in enumerate(not_color):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=estimators, colors=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_element_dtype_colors(estimators, not_list_of_colors):
    for i, v in enumerate(not_list_of_colors):
        with pytest.raises(AssertionError) as e:
            CellClasses(models=estimators, colors=v)
        assert "Invalid dtype" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_correct_models(estimators):
    clusters = CellClasses(models=estimators)
    expect = {i: v for i, v in enumerate(estimators)}
    assert clusters.models == expect, \
        "invalid value for self.models"


def test_correct_grns(estimators):
    clusters = CellClasses(models=estimators)
    expect = {i: v.get_matrix() for i, v in enumerate(estimators)}
    assert clusters.grns == expect, \
        "invalid value for self.grns"
    for v in clusters.grns:
        is_grn_matrix(clusters.grns[v])


def test_correct_names(estimators, names):
    kwargs = {"models": estimators, "names": names[:3]}
    clusters = CellClasses(**kwargs)
    expect = {i: v for i, v in enumerate(names[:3])}
    assert clusters.names == expect, \
        "invalid value for self.names"


def test_correct_colors(estimators, colors):
    kwargs = {"models": estimators, "colors": colors[:3]}
    clusters = CellClasses(**kwargs)
    expect = {i: v for i, v in enumerate(colors[:3])}
    assert clusters.colors == expect, \
        "invalid value for self.colors"


def test_fetch_invalid_dtype(estimators, names, colors, not_id):
    kwargs = {"models": estimators, "names": names[:3], "colors": colors[:3]}
    clusters = CellClasses(**kwargs)
    for i, v in enumerate(not_id):
        with pytest.raises(AssertionError) as e:
            clusters.fetch(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_fetch_correct_return(estimators, names, colors):
    kwargs = {"models": estimators, "names": names[:3], "colors": colors[:3]}
    clusters = CellClasses(**kwargs)
    for i, v in enumerate(clusters.names):
        by_int = clusters.fetch(i)
        by_str = clusters.fetch(v)
        is_cellclass_dict(by_int)
        is_cellclass_dict(by_str)
        assert by_int == by_str, \
            f"test failed for {i}-th input {v}, inconsistency with {by_int} and {by_str}"
        assert np.all(by_int["grn"] == clusters.grns[i]), \
            f"failed for {i}-th, inconsistency with {by_int['grn']} and {clusters.grns[i]}"
        assert by_int["name"] == clusters.names[i], \
            f"failed for {i}-th, inconsistency with {by_int['name']} and {clusters.names[i]}"
        assert by_int["color"] == clusters.colors[i], \
            f"failed for {i}-th, inconsistency with {by_int['color']} and {clusters.colors[i]}"
