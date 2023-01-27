"""
pgmpy wrapper class for PC algorithm
"""
import pandas as pd
from pgmpy.estimators import PC as PGMPYPC

from grnet.abstract import Estimator
from grnet.dev import typechecker


class PC(Estimator):
    """
    pgmpy wrapper class for PC algorithm

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
        super().__init__(data, n, random_state)
        pass

    def estimate(
        self,
        variant: str = "stable",
        ci_test: str = "pearsonr",
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
        ci_test: str, default: "pearsonr",
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
        * grnet.abstract.Estimator: 
        """
        if max_cond_vars is not None:
            typechecker(max_cond_vars, int, "max_cond_vars")
        max_cond_vars=self.data.shape[1] if max_cond_vars is None else max_cond_vars
        self.model = PGMPYPC(
            data=self.data
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
        return super().get_matrix()
