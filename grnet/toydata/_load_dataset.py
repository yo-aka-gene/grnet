"""
function to load example data
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd

from grnet.dev import typechecker


parent = str(Path(__file__).resolve().parent)

_namelist = np.unique([
    v.split("/")[-1].split('_')[-1].split('.')[0] for v in glob.glob(
        f"{parent}/data/*"
    )
]).tolist()


if len(_namelist) == 1:
    _choice = _namelist[0]
elif len(_namelist) == 2:
    _choice = " or ".join(_namelist)
else:
    _choice = ', '.join(_namelist[:-1]) + ', or ' + _namelist[-1]


def available_name():
    """
    Parameters
    ----------
    None

    Returns
    -------
    available names: List[str]
        list of names of available datasets
    """
    return _namelist


def load_dataset(
    name: str
) -> pd.core.frame.DataFrame:
    """
    Parameters
    ----------
    name: str
        name of dataset

    Returns
    -------
    dataset :pd.core.frame.DataFrame
        :math:`\\log_2(RPM+1)` data matrix

    Examples
    --------
    >>> import pandas as pd
    >>> from grnet.toydata import load_dataset
    >>> df = load_dataset("prototype1")
    >>> isinstance(df, pd.core.frame.DataFrame)
    True
    >>> df.shape
    (1000, 10000)
    """
    typechecker(name, str, "name")
    assert name in _namelist, \
        f"Invalid dataset name {name}. Choose from {_choice}."
    return pd.read_csv(
        f"{parent}/data/dataset_{name}.csv",
        index_col=0
    )


def load_metadata(
    name: str
) -> pd.core.frame.DataFrame:
    """
    Parameters
    ----------
    name: str
        name of dataset

    Returns
    -------
    dataset :pd.core.frame.DataFrame
        metadata matrix

    Examples
    --------
    >>> import pandas as pd
    >>> from grnet.toydata import load_metadata
    >>> df = load_metadata("prototype1")
    >>> isinstance(df, pd.core.frame.DataFrame)
    True
    >>> df.shape
    (1000, 1)
    """
    typechecker(name, str, "name")
    assert name in _namelist, \
        f"Invalid dataset name {name}. Choose from {_choice}."
    return pd.read_csv(
        f"{parent}/data/metadata_{name}.csv",
        index_col=0
    )
