"""
test for functions in grnet.dev._not_type.py
"""
from itertools import combinations

import numpy as np
import pandas as pd
import pytest


from grnet.dev import invalid_types


@pytest.fixture
def list_of_values():
    return [
        "a", 0, 1.1, 1+4j, np.ones(10)[1], np.pi,
        True, type, lambda x:x, [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]


@pytest.fixture
def types():
    return [
        str, int, float, complex, np.int64, np.float64,
        bool, type, type(lambda x:x), list, dict, np.ndarray,
        pd.core.frame.DataFrame, pd.core.indexes.base.Index
    ]


@pytest.fixture
def tuple_of_types():
    return [
        v for v in combinations(types(), 2)
    ]


@pytest.fixture
def not_type():
    return [str(t) for t in types()]


def invalid_inputs(not_type):
    for i, v in not_type:
        with pytest.raises(AssertionError) as e:
            invalid_types(v)
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def valid_input_type(types):
    for i, v in types:
        expect = [t for t in list_of_values() if not isinstance(t, v)]
        ret = invalid_types(v)
        assert ret == expect, \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"


def valid_input_tuples(tuple_of_types):
    for i, v in enumerate(tuple_of_types):
        expect = [t for t in list_of_values() if not isinstance(t, v)]
        ret = invalid_types(v)
        assert ret == expect, \
            f"invalid return values in {i}-th input\nexpected: {expect}\ngot: {ret}"
