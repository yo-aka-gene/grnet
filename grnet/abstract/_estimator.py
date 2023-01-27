"""
Abstract class for wrapper classes of pgmpy.estimators
"""
from itertools import combinations

import numpy as np
import pandas as pd


from grnet.dev import typechecker, valchecker

class Estimator:
    """
    Abstract class for wrapper classes of pgmpy.estimators

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
        self,
        **kwargs
    ) -> None:
        estimate network and save edges (a list of tuples) as self.edges

    get_matrix(
        self
    ) -> pandas.core.frame.DataFrame:
        export network information as DxD matrix of 0 or 1 elements

    Attributes
    ----------
    data: pandas.core.frame.DataFrame
        input data or resampled data
        (data will be resampled if `n` is specified in `self.__init__`)

    edges: List[tuple]
        information of edges are saved as a list of tuples
        after `self.estimate` was run
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
            NxD matrix (N: number of samples, D: number of genes) of data

        n: int, default: None
            positive integer for resampling (for n > N, N will be used instead)
            if None, resampling will not be performed

        random_state: int, default: 0
            random seed for random sampling

        Returns
        -------
        None
        """
        typechecker(data, pd.core.frame.DataFrame, "data")
        if n is not None:
            typechecker(n, int, "n")
            valchecker(n>0, "n should be a positive integer")
        typechecker(random_state, int, "random_state")
        np.random.seed(random_state)
        self.data = data if n is None else data.sample(n=min(n, len(data)))
        pass

    def estimate(
        self,
        **kwargs
    ) -> None:
        """
        Parameters
        ----------
        **kwargs
            kwargs for corresponding classes of pgmpy.estimators

        Returns
        -------
        None
        """
        self.edges = []
        typechecker(self.edges, list, "self.edges")
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
        df = pd.DataFrame(
            np.eye(self.data.shape[1]),
            index=self.data.columns,
            columns=self.data.columns
        )
        for i, v in combinations(df.columns, 2):
            df.loc[i, v] = 1 if (i, v) in self.edges or (v, i) in self.edges else 0
        
        typechecker(df, pd.core.frame.DataFrame, "df")
        return df
