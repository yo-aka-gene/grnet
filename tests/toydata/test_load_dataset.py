"""
Test for grnet.dataset._load_dataset.py
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from grnet.toydata import available_name, load_dataset, load_metadata
from grnet.dev import typemolds


@pytest.fixture
def not_str():
    return typemolds(str)


@pytest.fixture
def correct_names():
    root = str(Path(__file__).resolve().parent.parent.parent)
    ret = np.unique([
        v.split("/")[-1].split('_')[-1].split('.')[0] for v in glob.glob(
            f"{root}/grnet/dataset/data/*"
        )
    ]).tolist()
    return ret


@pytest.fixture
def invalid_names():
    return [
        "not_data", "invalid", "incorrect"
    ]


def test_available_name_correct_return(correct_names):
    assert available_name() == correct_names, \
        f"test failed\nrequired: {correct_names}\ngot: {available_name()}"


def test_load_dataset_invalid_dtype(not_str):
    for i, v in enumerate(not_str):
        with pytest.raises(AssertionError) as e:
            load_dataset(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_load_dataset_invalid_name(invalid_names):
    for i, v in enumerate(invalid_names):
        with pytest.raises(AssertionError) as e:
            load_dataset(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_load_dataset_correct_return(correct_names):
    for i, v in enumerate(correct_names):
        assert isinstance(load_dataset(v), pd.core.frame.DataFrame), \
            f"test failedd for {i}-th input {v}"


def test_load_metadata_invalid_dtype(not_str):
    for i, v in enumerate(not_str):
        with pytest.raises(AssertionError) as e:
            load_metadata(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_load_metadata_invalid_name(invalid_names):
    for i, v in enumerate(invalid_names):
        with pytest.raises(AssertionError) as e:
            load_metadata(v)
        assert f"{v}" in f"{e.value}", \
            f"test failed for {i}-th input {v}"


def test_load_metadata_correct_return(correct_names):
    for i, v in enumerate(correct_names):
        assert isinstance(load_metadata(v), pd.core.frame.DataFrame), \
            f"test failedd for {i}-th input {v}"
