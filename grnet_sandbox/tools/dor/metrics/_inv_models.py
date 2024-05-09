import numpy as np
from sklearn.metrics import mean_absolute_error as mae
from statsmodels.genmod.generalized_linear_model import GLMResultsWrapper

from grnet.dev import AlgebraicArrays, typechecker


def horizontal_mae(
    x: AlgebraicArrays,
    y: AlgebraicArrays,
    model: GLMResultsWrapper,
    avoid_inf: bool = True
) -> np.ndarray:
    typechecker(x, AlgebraicArrays, "x")
    typechecker(y, AlgebraicArrays, "y")
    typechecker(model, GLMResultsWrapper, "model")
    typechecker(avoid_inf, bool, "avoid_inf")
    y_intercep, coeff = model.params
    inv = lambda y: (
        (np.log(y) - y_intercep) / coeff
    )
    return mae(
        x[np.where(y != 0)] if avoid_inf else x,
        np.frompyfunc(inv, 1, 1)(y[np.where(y != 0)] if avoid_inf else y)
    )


def horizontal_maxae(
    x: AlgebraicArrays,
    y: AlgebraicArrays,
    model: GLMResultsWrapper,
    avoid_inf: bool = True
) -> np.ndarray:
    typechecker(x, AlgebraicArrays, "x")
    typechecker(y, AlgebraicArrays, "y")
    typechecker(model, GLMResultsWrapper, "model")
    typechecker(avoid_inf, bool, "avoid_inf")
    y_intercep, coeff = model.params
    inv = lambda y: (
        (np.log(y) - y_intercep) / coeff
    )
    return np.abs(
        x[np.where(y != 0)] - np.frompyfunc(inv, 1, 1)(y[np.where(y != 0)])
    ).max() if avoid_inf else np.abs(
        x - np.frompyfunc(inv, 1, 1)(y)
    ).max()
