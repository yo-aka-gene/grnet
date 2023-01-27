"""
test for functions in grnet.dev._typemolds.py
"""
from itertools import combinations

import numpy as np
import pandas as pd
import pytest

from grnet.dev import typemolds


def list_of_values():
    return [
        "a", 0, 1.1, 1+4j, np.ones(10)[1], np.pi,
        True, type, (), [], {}
    ]


def list_of_arraylike():
    return [
        np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]


def _types():
    return [
        str, int, float, complex, np.int64, np.float64,
        bool, type, tuple, list, dict
    ]


@pytest.fixture
def types():
    return [
        str, int, float, complex, np.int64, np.float64,
        bool, type, tuple, list, dict
    ]


def _arraylike():
    return [
        np.ndarray,
        pd.core.frame.DataFrame,
        pd.core.indexes.base.Index
    ]


@pytest.fixture
def arraylike():
    return [
        np.ndarray,
        pd.core.frame.DataFrame,
        pd.core.indexes.base.Index
    ]


@pytest.fixture
def tuple_of_types():
    return [
        v for v in combinations(_types(), 2)
    ]


@pytest.fixture
def tuple_of_arraylike():
    return [
        v for v in combinations(_arraylike(), 2)
    ]


@pytest.fixture
def not_type():
    return [str(t) for t in _types()]


def test_invalid_inputs(not_type):
    for i, v in enumerate(not_type):
        with pytest.raises(AssertionError) as e:
            typemolds(v)
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def test_valid_input_type(types):
    for i, v in enumerate(types):
        exclude = (v, *_arraylike())
        expect = [t for t in list_of_values() if not isinstance(t, exclude)]
        ret = typemolds(exclude)
        assert ret == expect, \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"


def test_valid_input_arraylike(arraylike):
    for i, v in enumerate(arraylike):
        exclude = (v,  *_types())
        expect = [t for t in list_of_arraylike() if not isinstance(t, exclude)]
        ret = typemolds(exclude)
        assert len(expect) == len(ret), \
            f"invalid return length in {i}-th input\nexpected: {expect}\ngot: {ret}"
        assert np.all([np.all(r == e) for r, e in zip(ret, expect)]), \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"


def test_valid_input_tuples(tuple_of_types):
    for i, v in enumerate(tuple_of_types):
        exclude = (*v, *_arraylike())
        expect = [t for t in list_of_values() if not isinstance(t, exclude)]
        ret = typemolds(exclude)
        assert ret == expect, \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"


def test_valid_input_tuples_of_arraylike(tuple_of_arraylike):
    for i, v in enumerate(tuple_of_arraylike):
        exclude = (*v,  *_types())
        expect = [t for t in list_of_arraylike() if not isinstance(t, exclude)]
        ret = typemolds(exclude)
        assert len(expect) == len(ret), \
            f"invalid return length in {i}-th input\nexpected: {expect}\ngot: {ret}"
        assert np.all([np.all(r == e) for r, e in zip(ret, expect)]), \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"
