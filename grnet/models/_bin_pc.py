"""
pgmpy wrapper class for PC algorithm
"""
import numpy as np
import pandas as pd
from pgmpy.estimators import PC as PGMPYPC

from grnet.abstract import Estimator
from grnet.dev import typechecker


class BinPC(Estimator):
    """
    pgmpy wrapper class for PC algorithm with DOR-based binarization

    Methods
    -------
    __init__(
        self,
        data: pandas.DataFrame,
        n: int,
        random_state: int
    ) -> None:
        initialize attributes

    estimate(
        self,
        variant: str,
        ci_test: str,
        max_cond_vars: int,
        return_type: str,
        significance_level: float,
        n_jobs: int,
        show_progress: bool
    ) -> None:
        estimate network and save edges (a list of tuples) as self.edges by PC algorithm
        actual implementation of PC algorithm is a wrapper of pgmpy.estimators.PC
        default values are altered from the original codes for some arguments to adjust for GRNs

    get_matrix(
        self
    ) -> pandas.core.frame.DataFrame:
        export network information as DxD matrix of 0 or 1 elements

    Attributes
    ----------
    data: pandas.core.frame.DataFrame
        input data or resampled data
        (data will be resampled if `n` is specified in `self.__init__`)

    model: pgmpy.estimators.PC.PC
        model information (for debugging)

    edges: List[tuple]
        information of edges are saved as a list of tuples
        after `self.estimate` was run

    References
    ----------
    * pgmpy.estimators.PC: https://pgmpy.org/structure_estimator/pc.html?highlight=pc
    """
    def __init__(
        self,
        data: pd.DataFrame,
        n: int = None,
        random_state: int = 0
    ) -> None:
        """
        Parameters
        ----------
        data: pandas.DataFrame
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
        super().__init__(data, n, random_state)
        pass

    def estimate(
        self,
        variant: str = "stable",
        ci_test: str = "chi_square",
        max_cond_vars: int = None,
        return_type: str = "dag",
        significance_level: float = 0.01,
        n_jobs: int = -1,
        show_progress: bool = False
    ) -> None:
        """
        Parameters
        ----------
        variant: str, default: "stable",
        ci_test: str, default: "chi_square",
        max_cond_vars: int, default: None,
        return_type: str, default: "dag",
        significance_level: float, default: 0.01,
        n_jobs: int, default: -1,
        show_progress: bool, default: False

        Returns
        -------
        None

        References
        ----------
        * pgmpy.estimators.PC: https://pgmpy.org/structure_estimator/pc.html?highlight=pc
        * grnet.abstract.Estimator: https://grnet.readthedocs.io/en/latest/grnet.abstract.html#grnet.abstract.Estimator
        """
        if max_cond_vars is not None:
            typechecker(max_cond_vars, int, "max_cond_vars")
        max_cond_vars = self.data.shape[1] if max_cond_vars is None else max_cond_vars
        self.model = PGMPYPC(
            data=(self.data != 0).astype(int)
        )
        model = self.model.estimate(
            variant=variant,
            ci_test=ci_test,
            max_cond_vars=max_cond_vars,
            return_type=return_type,
            significance_level=significance_level,
            n_jobs=n_jobs,
            show_progress=show_progress
        )
        self.edges = list(model.edges)
        pass

    def get_matrix(
        self
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        None

        Returns
        -------
        GRNMatrix: pandas.DataFrame
            edge information of the GRN will be returned as a DxD matrix

        References
        ----------
        * grnet.abstract.Estimator: https://grnet.readthedocs.io/en/latest/grnet.abstract.html#grnet.abstract.Estimator
        """
        mat = super().get_matrix().values
        mat[np.diag_indices_from(mat)] = (self.data != 0).astype(int).sum() / len(self.data)
        return pd.DataFrame(
            mat,
            index=self.data.columns,
            columns=self.data.columns
        )
