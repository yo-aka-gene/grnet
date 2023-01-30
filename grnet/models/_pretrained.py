"""
class for pretrained matrix
"""
import numpy as np
import pandas as pd

from grnet.abstract import Estimator
from grnet.dev import is_grn_matrix


class PretrainedModel(Estimator):
    """
    class for pretrained GRN matrix (to be treated as a subclass of `Estimator`)

    Methods
    -------
    __init__(
        self,
        data: pandas.core.frame.DataFrame,
        n: int,
        random_state: int
    ) -> None:
        initialize attributes

    estimate(
        self
    ) -> None:
        always ignored (preserved for consistency)

    get_matrix(
        self
    ) -> pandas.core.frame.DataFrame:
        returns the original GRN matrix

    Attributes
    ----------
    data: pandas.core.frame.DataFrame
        GRN matrix

    edges: List[tuple]
        information of edges are saved as a list of tuples

    References
    ----------
    * grnet.abstract.Estimator: https://grnet.readthedocs.io/en/latest/grnet.abstract.html#grnet.abstract.Estimator
    """
    def __init__(
        self,
        data: pd.core.frame.DataFrame,
        n: int = None,
        random_state: int = 0
    ) -> None:
        """
        Parameters
        ----------
        data: pandas.core.frame.DataFrame
            pretrained GRN matrix

        n: int, default: None
            always ignored (preserved for consistency)

        random_state: int, default: 0
            always ignored (preserved for consistency)

        Returns
        -------
        None
        """
        is_grn_matrix(data=data)
        super().__init__(data, n, random_state)
        feat = data.columns
        self.edges = [
            (feat[idx], feat[col]) for idx, col in zip(*np.where(data == 1)) if idx != col
        ]
        pass

    def estimate(
        self
    ) -> None:
        """
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass

    def get_matrix(
        self
    ) -> pd.core.frame.DataFrame:
        """
        Parameters
        ----------
        None

        Returns
        -------
        GRNMatrix: pandas.core.frame.DataFrame
            edge information of the GRN will be returned as a DxD matrix
        """
        return self.data
