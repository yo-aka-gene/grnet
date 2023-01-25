"""
test for functions in grnet.dev._checker.py
"""
from itertools import combinations

import numpy as np
import pandas as pd
import pytest

from grnet.dev import typechecker, valchecker


def _values():
    return [
        "a", 0, 1.1, 1+4j, np.ones(10).astype(np.int64)[1], np.pi,
        True, [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]


@pytest.fixture
def values():
    return [
        "a", 0, 1.1, 1+4j, np.ones(10).astype(np.int64)[1], np.pi,
        True, [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]


@pytest.fixture
def not_str():
    return [
        0, 1.1, 1+4j, np.ones(10)[1], np.pi,
        True, type, lambda x:x, (), [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]

@pytest.fixture
def tuple_of_types():
    return [
        (str, type(v)) for v in _values()
    ]


@pytest.fixture
def not_bool():
    return [
        "a", 0, 1.1, 1+4j, np.ones(10)[1], np.pi,
        type, lambda x:x, (), [], {}, np.zeros(5),
        pd.DataFrame(np.eye(2), index=["a1", "a2"], columns=["b1", "b2"]),
        pd.DataFrame(np.eye(2), index=["a", "b"]).index
    ]


@pytest.fixture
def trues():
    return [
        True, 1 == 1, (np.ones([1]) == 1)[0]
    ]


@pytest.fixture
def falses():
    return [
        False, 1 == 0, (np.ones([1]) == 0)[0]
    ]


def test_type_invalid_input_for_types(values):
    for i, v in enumerate(values):
        with pytest.raises(AssertionError) as e:
            typechecker("var", v, "name")
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def test_type_invalid_input_for_varname(not_str):
    for i, v in enumerate(not_str):
        with pytest.raises(AssertionError) as e:
            typechecker("var", str, v)
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def test_type_invalid_type_declaration(values):
    for i, v in enumerate(values):
        wrong_type = type(_values()[0]) if i == len(_values()) - 1 else type(_values()[i+1])
        print(v, wrong_type)
        with pytest.raises(AssertionError) as e:
            typechecker(v, wrong_type, "name")
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and required type is {wrong_type}\n\
                while the output is {e.values}"


def test_type_correct_input_values(values):
    for i, v in enumerate(values):
        assert typechecker(v, type(v), "name") is None, \
            f"Failed when the {i}-th input is {v}"


def test_type_correct_type_declaration_with_tuples(tuple_of_types):
    for i, v in enumerate(tuple_of_types):
        assert typechecker("a", v, "name") is None, \
            f"Failed when the {i}-th input is {v}"


def test_type_correct_error_msg(values):
    for i, v in enumerate(values):
        wrong_type = type(_values()[0]) if i == len(_values()) - 1 else type(_values()[i+1])
        with pytest.raises(AssertionError) as e:
            typechecker(v, wrong_type, "asdfghjkl")
        assert f"{wrong_type}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}\n\
                while {wrong_type} should be there"
        assert "asdfghjkl" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}\n\
                while asdfghjkl should be there"


def test_type_correct_error_msg_with_tuples(tuple_of_types):
    for i, v in enumerate(tuple_of_types):
        with pytest.raises(AssertionError) as e:
            typechecker(lambda x:x, v, "asdfghjkl")
        assert np.all([f"{t}" in f"{e.value}" for t in v]), \
            f"Failed when the {i}-th input is {v} while error msg should include all types"
        assert "asdfghjkl" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}\n\
                while asdfghjkl should be there"


def test_val_invalid_input(not_bool):
    for i, v in enumerate(not_bool):
        with pytest.raises(AssertionError) as e:
            valchecker(v)
        assert f"{v}" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def test_val_correct_input_true(trues):
    for i, v in enumerate(trues):
        assert valchecker(v) is None, \
            f"invalid return value for {i}-th input\nexpected: {None}\n got: {valchecker(v)}"


def test_val_correct_input_false(falses):
    for i, v in enumerate(falses):
        with pytest.raises(AssertionError) as e:
            valchecker(v)
        assert "Invalid" in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"


def test_val_correct_suffix(falses):
    suffix = "asdfghjkl"
    for i, v in enumerate(falses):
        with pytest.raises(AssertionError) as e:
            valchecker(v, suffix=suffix)
        assert suffix in f"{e.value}", \
            f"Failed when the {i}-th input is {v} and the output is {e.values}"
