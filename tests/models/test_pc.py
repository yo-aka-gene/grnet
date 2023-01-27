"""
Test module for PC
"""
import numpy as np
import pandas as pd
from pgmpy.estimators import PC as PGMPYPC
import pytest

from grnet.abstract import Estimator
from grnet.dev import typemolds
from grnet.models import PC


@pytest.fixture
def not_df():
    return typemolds(pd.core.frame.DataFrame)


@pytest.fixture
def not_int():
    return typemolds(int)


@pytest.fixture
def not_pos_int():
    return [
        0, -10, -np.pi, np.e
    ]


@pytest.fixture
def dfs():
    rows = [f"a{i}" for i in range(15)]
    cols = [f"b{i}" for i in range(5)]
    df = pd.DataFrame(np.random.randint(1, 10, (15, 5)), index=rows, columns=cols)
    return [
        df
    ]


def test_init_invalid_dtype_data(not_df):
    for i, v in enumerate(not_df):
        with pytest.raises(AssertionError) as e:
            PC(data=v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input: {e.value}"


def test_init_invalid_dtype_n(not_int):
    df = pd.DataFrame(np.eye(2), index=["a", "b"], columns=["c", "d"])
    for i, v in enumerate(not_int):
        with pytest.raises(AssertionError) as e:
            PC(data=df, n=v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input: {e.value}"


def test_init_invalid_value_n(not_pos_int):
    df = pd.DataFrame(np.eye(2), index=["a", "b"], columns=["c", "d"])
    for i, v in enumerate(not_pos_int):
        with pytest.raises(AssertionError) as e:
            PC(data=df, n=v)
        assert "Invalid" in f"{e.value}", \
            f"test failed for {i}-th input: {e.value}"


def test_init_invalid_dtype_random_state(not_int):
    df = pd.DataFrame(np.eye(2), index=["a", "b"], columns=["c", "d"])
    for i, v in enumerate(not_int):
        with pytest.raises(AssertionError) as e:
            PC(data=df, random_state=v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input: {e.value}"


def test_init_correct_subclass(dfs):
    for i, v in enumerate(dfs):
        model = PC(data=v)
        assert isinstance(model, Estimator), \
            f"test failed for {i}-th input: PC should inherit grnet.Estimator, got {model}[{type(model)}]"


def test_init_correct_attribute_dtype(dfs):
    for i, v in enumerate(dfs):
        model = PC(data=v)
        assert isinstance(model.data, pd.core.frame.DataFrame), \
            f"test failed for {i}-th input: self.data should be a DataFrame, got {v}[{type(v)}]"


def test_init_correct_df_size():
    df = pd.DataFrame(np.eye(5))
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        model = PC(data=df, n=i)
        shape = (min(i, df.shape[0]), df.shape[1])
        assert model.data.shape == shape, \
            f"test failed for {i}-th input: self.data.shape expected {shape}, got {model.data.shape}"
    model = PC(data=df)
    shape = df.shape
    assert model.data.shape == shape, \
        f"test failed for n=None: self.data.shape expected {shape}, got {model.data.shape}"


def test_init_random_seed_fixation():
    df = pd.DataFrame(np.eye(15))
    for i in range(10):
        ret = PC(data=df, n=7, random_state=i).data
        expected = PC(data=df, n=7, random_state=i).data
        assert np.all(ret == expected), \
            f"test failed for {i}-th input: inconsistency in self.data by runs"


def test_estimate_correct_return(dfs):
    for i, v in enumerate(dfs):
        model = PC(data=v)
        model.estimate()
        ret = model.edges
        assert isinstance(ret, list), \
            f"test failed for {i}-th input: model.edges should be list, got {ret}[{type(ret)}]"
        for i_e, e in enumerate(ret):
            assert isinstance(e, tuple), \
                f"test failed for {i}-th input: got {e}[{type(e)}] in {i_e}-th element"
            assert len(e) == 2, \
                f"test failed for {i}-th input: got {e} in {i_e}-th element"


def test_estimate_correct_models(dfs):
    for i, v in enumerate(dfs):
        model = PC(data=v)
        model.estimate()
        att = model.model
        assert isinstance(att, PGMPYPC), \
            f"test failed for {i}-th input: model.edges should be a pgmpy.estimators.PC.PC,\
                 got {att}[{type(att)}]"


def test_get_matrix_correct_order(dfs):
    for v in dfs:
        model = PC(data=v)
        with pytest.raises(AttributeError):
            model.get_matrix()


def test_get_matrix_correct_return_dtype(dfs):
    for i, v in enumerate(dfs):
        model = PC(data=v)
        model.estimate()
        ret = model.get_matrix()
        assert isinstance(ret, pd.core.frame.DataFrame), \
            f"test failed for {i}-th input: return value should be a DataFrame, got {ret}[{type(ret)}]"
        assert np.all((ret == 0) + (ret == 1)), \
            f"test failed for {i}-th input: elements sould be 0 or 1, got {ret}"


def test_get_matrix_correct_return_shape():
    rows = [f"a{i}" for i in range(15)]
    cols = [f"b{i}" for i in range(5)]
    df = pd.DataFrame(np.random.randint(1, 10, (15, 5)), index=rows, columns=cols)
    for i in [3, 4, 5, 6, 7, 8, 9, 10]:
        model = PC(data=df, n=i)
        model.estimate()
        ret = model.get_matrix()
        shape = (5, 5)
        assert ret.shape == shape, \
            f"test failed for {i}-th input: got {ret} [{ret.shape}] while a {shape} matrix is expected"


def test_get_matrix_correct_return_rows_cols():
    rows = [f"a{i}" for i in range(15)]
    cols = [f"b{i}" for i in range(5)]
    df = pd.DataFrame(np.random.randint(1, 10, (15, 5)), index=rows, columns=cols)
    for i in [3, 4, 5, 6, 7, 8, 9, 10]:
        model = PC(data=df, n=i)
        model.estimate()
        ret = model.get_matrix()
        assert np.all(ret.index == cols), \
            f"test failed for {i}-th input: got {ret} while required idx name is {cols}"
        assert np.all(ret.columns == cols), \
            f"test failed for {i}-th input: got {ret} while required cols name is {cols}"
