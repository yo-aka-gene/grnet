"""
Class to manage cell classes in in a dataset
"""
from typing import Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd

from grnet.abstract import Estimator
from grnet.dev import is_grn_matrix, typechecker, valchecker


class CellClasses:
    """
    Class to manage cell classes in in a dataset

    Methods
    -------
    __init__(
        self,
        models: List[grnet.abstract.Estimator],
        names: List[Union[str, int]],
        colors: Union[List[Union[Tuple[float], str]], str]
    ) -> None:
        initialize attributes

    fetch(
        self,
        id: Union[int, str]
    ) -> Dict[str, Union[pd.core.frame.DataFrame, str, int, Tuple[float]]]:
        fetch a set of information about a cell class (cell-class dict)

    Attributes
    ----------
    models: Dict[int, grnet.abstract.Estimator]
        referring the input list of pretrained (self.estiamte() is already run) models
         for the cell classes, cell classes are saved with indexes

    grns: Dict[int, pandas.core.frame.DataFrame]
        referring the input list of pretrained (self.estiamte() is already run) models
         for the cell classes, GRN matrices of the cell classes are saved with indexes

    names: Dict[int, Union[str, int]]
        referring the input list of names for the cell classes,
         cell classes are saved with indexes

    colors: Dict[int, Union[str, Tuple[float]]]
        referring the input list of colors (used in visualization) for the cell classes,
         cell classes are saved with indexes
    """
    def __init__(
        self,
        models: List[Estimator],
        names: List[Union[str, int]] = None,
        colors: Union[List[Union[Tuple[float], str]], str] = None,
    ) -> None:
        """
        Parameters
        ----------
        models: List[grnet.abstract.Estimator]
            list of pretrained (self.estiamte() is already run) models for the cell classes

        names: List[Union[str, int]], default: None
            list of names for the cell classes. \
            required to have the same length with `models`

        colors: Union[List[Union[Tuple[float], str]], str], default: None
            list of colors (used in visualization) for the cell classes \
            required to have the same length with `models`

        Returns
        -------
        None
        """
        typechecker(models, list, "models")
        for i, v in enumerate(models):
            typechecker(v, Estimator, f"models[{i}]")
            is_grn_matrix(v.get_matrix())
        self.models = {i: v for i, v in enumerate(models)}
        self.grns = {i: v.get_matrix() for i, v in enumerate(models)}
        if names is None:
            self.names = {i: i for i in range(len(models))}
        else:
            typechecker(names, list, "names")
            valchecker(
                len(names) == len(models),
                "Length of `names` should be equal to the length of `models`"
            )
            for i, v in enumerate(names):
                typechecker(v, (str, int), f"names[{i}]")
            self.names = {i: v for i, v in enumerate(names)}
        if colors is None:
            self.colors = {
                i: f"C{i}" for i in range(len(models))
            } if len(models) <= 10 else {
                i: plt.cm.jet(i/len(models)) for i in range(len(models))
            }
        else:
            typechecker(colors, (list, str), "colors")
            if isinstance(colors, list):
                valchecker(
                    len(colors) == len(models),
                    "Length of `names` should be equal to the length of `models`"
                )
                for i, v in enumerate(colors):
                    typechecker(v, (tuple, str), f"colors[{i}]")
                    if isinstance(v, tuple):
                        valchecker(len(v) == 4, f"Length of colors[{i}] should be 4")
                        for i_el, el in enumerate(v):
                            typechecker(el, float, f"colors[{i}][{i_el}]")

                self.colors = {i: v for i, v in enumerate(colors)}
            else:
                self.colors = {
                    i: eval(f"plt.cm.{colors}")(i / len(models)) for i in range(len(models))
                }
        return None

    def fetch(
        self,
        id: Union[int, str]
    ) -> Dict[str, Union[pd.core.frame.DataFrame, str, int, Tuple[float]]]:
        """
        Parameters
        ----------
        id: Union[int, str]
            index or name of the cell class

        Returns
        -------
        cell-class dict: Dict[str, Union[pd.core.frame.DataFrame, str, int, Tuple[float]]]
            {"grn": pd.core.frame.DataFrame, "name": Union[str, int], "color": Union[str, Tuple[float]]}
        """
        typechecker(id, (str, int), "id")
        if isinstance(id, str):
            temp = {self.names[v]: v for v in self.names}
            id = temp[id]
        return {"grn": self.grns[id], "name": self.names[id], "color": self.colors[id]}
