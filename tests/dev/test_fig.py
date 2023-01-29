"""
Tests for grnet.dev._fig.py
"""
import pytest

from grnet.dev import kwarg_mgr, typemolds


@pytest.fixture
def not_dict():
    return typemolds(dict)


@pytest.fixture
def not_str():
    return typemolds(str)


@pytest.fixture
def not_type():
    return typemolds((type, tuple))


@pytest.fixture
def not_tuple_of_types(not_type):
    return [(type, v) for v in not_type]


@pytest.fixture
def types():
    return [type(v) for v in typemolds(type)] + [type]


@pytest.fixture
def tuple_of_types(types):
    return [(type, v) for v in types]


def test_invalid_kwargs(not_dict):
    for i, v in enumerate(not_dict):
        with pytest.raises(AssertionError) as e:
            kwarg_mgr(kwargs=v, key="a", default=None)
        assert "kwargs" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_key(not_str):
    for i, v in enumerate(not_str):
        with pytest.raises(AssertionError) as e:
            kwarg_mgr(kwargs={}, key=v, default=None)
        assert "key" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_typehint(not_type):
    for i, v in enumerate(not_type):
        with pytest.raises(AssertionError) as e:
            kwarg_mgr(kwargs={"asdf": type}, key="asdf", default=None, typehint=v)
        assert "typehint" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_invalid_typehint_tuple(not_tuple_of_types):
    for i, v in enumerate(not_tuple_of_types):
        with pytest.raises(AssertionError) as e:
            kwarg_mgr(kwargs={"asdf": 1}, key="asdf", default=None, typehint=v)
        assert "typehint" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_not_found():
    kwargs = [
        {},
        {f"a{i}": i for i in range(5)}
    ]
    for i, v in enumerate(kwargs):
        ret = kwarg_mgr(kwargs=v, key="asdf", default=None)
        assert ret is None, \
            f"test failed for {i}-th input: expected None, got {ret}"


def test_found():
    kwargs = [
        {"asdf": "ghjk"},
        {**{f"a{i}": i for i in range(5)}, "asdf": "ghjk"}
    ]
    for i, v in enumerate(kwargs):
        ret = kwarg_mgr(kwargs=v, key="asdf", default=None)
        assert ret  == "ghjk", \
            f"test failed for {i}-th input: expected 'ghjk', got {ret}"


def test_not_found_and_typecheck():
    kwargs = [
        {},
        {f"a{i}": i for i in range(5)}
    ]
    for i, v in enumerate(kwargs):
        ret = kwarg_mgr(kwargs=v, key="asdf", default=None, typehint=int)
        assert ret is None, \
            f"test failed for {i}-th input: expected None, got {ret}"


def test_found_and_invalid_type():
    kwargs = [
        {"asdf": "ghjk"},
        {**{f"a{i}": i for i in range(5)}, "asdf": "ghjk"}
    ]
    for i, v in enumerate(kwargs):
        with pytest.raises(AssertionError) as e:
            kwarg_mgr(kwargs=v, key="asdf", default=1, typehint=int)
        assert "asdf" in f"{e.value}", \
            f"test failed for {i}-th input"


def test_found_and_typecheck():
    kwargs = [
        {"asdf": "ghjk"},
        {**{f"a{i}": i for i in range(5)}, "asdf": "ghjk"}
    ]
    for i, v in enumerate(kwargs):
        ret = kwarg_mgr(kwargs=v, key="asdf", default=None, typehint=str)
        assert ret == "ghjk", \
            f"test failed for {i}-th input: expected 'ghjk', got {ret}"
