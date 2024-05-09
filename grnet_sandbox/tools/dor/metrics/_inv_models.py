from typing import Callable

import numpy as np
from sklearn.metrics import mean_absolute_error as mae

from grnet.dev import AlgebraicArrays, typechecker


def horizontal_mae(
    x: AlgebraicArrays,
    y: AlgebraicArrays,
    inv_model: Callable,
    avoid_inf: bool = True
) -> np.ndarray:
    typechecker(x, AlgebraicArrays, "x")
    typechecker(y, AlgebraicArrays, "y")
    typechecker(inv_model, Callable, "inv_model")
    typechecker(avoid_inf, bool, "avoid_inf")
    return mae(
        x[np.where(y != 0)] if avoid_inf else x,
        np.frompyfunc(inv_model, 1, 1)(y[np.where(y != 0)] if avoid_inf else y)
    )


def horizontal_maxae(
    x: AlgebraicArrays,
    y: AlgebraicArrays,
    inv_model: Callable,
    avoid_inf: bool = True
) -> np.ndarray:
    typechecker(x, AlgebraicArrays, "x")
    typechecker(y, AlgebraicArrays, "y")
    typechecker(inv_model, Callable, "inv_model")
    typechecker(avoid_inf, bool, "avoid_inf")
    return np.abs(
        x[np.where(y != 0)] - np.frompyfunc(inv_model, 1, 1)(y[np.where(y != 0)])
    ).max() if avoid_inf else np.abs(
        x - np.frompyfunc(inv_model, 1, 1)(y)
    ).max()
