from typing import Callable, Union

import anndata as ad
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

from grnet.anndata.preprocessing import binarize
from sklearn.metrics import r2_score, mean_squared_error

from ._abstract import DORModel


class LogisticModel(DORModel):
    def __init__(
        self,
        random_state: int = 0,
        n_trials: int = 100
    ) -> None:
        super().__init__(
            name="LM",
            random_state=random_state,
            n_trials=n_trials
        )
        return None


    def fit(
        self,
        data: ad.AnnData,
        optimizer: str = "Adagrad",
        lr: float = .1
    ) -> None:
        super().fit(
            data=data,
            formula="$y=-2/(1+e^{-b\cdot Mean})+2$"
        )
        torch.manual_seed(self.seed)
        b = torch.rand(1, requires_grad=True)
        x = torch.from_numpy(data.var["Mean"].values)
        y = torch.from_numpy(data.var["DOR"].values)

        torch.manual_seed(self.seed)
        optimizer = eval(f"torch.optim.{optimizer}")([b], lr=lr)

        for _ in range(self.n_trials):
            fx = 2 - 2 / (1 + np.e ** (-b * x))
            obj = (
                (fx - y) ** 2
            ).sum()
            obj.backward()
            optimizer.step()
            optimizer.zero_grad()

        self.beta = b.item()
        self.mse = obj.item()
        self.x = x.numpy()
        self.y = y.numpy()
        self.f = lambda mean: 2 - 2 / (1 + np.e ** (-self.beta * mean))
        self.y_hat = self.f(self.x)
        self.mse = mean_squared_error(self.y, self.y_hat)
        self.r2_score = r2_score(self.y, 2 - 2 / (1 + np.e ** (-self.beta * self.x)))
        self.predict_mean = lambda dor: (
            (np.log(2 - dor) - np.log(dor)) / self.beta
        )


    def plot(
        self, 
        ax: plt.Axes = None,
        label: str = None,
        linelabel: str = "$y=-2x+2$",
        **kwargs
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        s = kwargs["s"] if "s" in kwargs else .1
        c = kwargs["c"] if "c" in kwargs else ".6"
        lc = kwargs["linecolor"] if "linecolor" in kwargs else "C0"
        digit = kwargs["round"] if "round" in kwargs else 3
        ndot = kwargs["ndot"] if "ndot" in kwargs else 1000
        ax.scatter(
            1 / (1 + np.e ** (-self.beta * self.x)), 
            self.y, s=s, c=c, label=label
        )
        x = np.linspace(0.5, 1, ndot)
        ax.plot(x, 2 - 2 * x, c=lc, label=linelabel)
        ax.set(
            xlabel="$1/(1+e^{-b\cdot Mean})$", ylabel="$DOR$", 
            title="$b="+f"{round(self.beta, digit)},"+"\;R^2="+f"{self.r2_score.round(digit)}$"
        )
        ax.legend()


    def residual_plot(
        self, 
        ax: plt.Axes = None,
        label: str = None,
        **kwargs
    ) -> None:
        if ax is None:
            _, ax = plt.subplots()
        s = kwargs["s"] if "s" in kwargs else .1
        c = kwargs["c"] if "c" in kwargs else ".6"
        lc = kwargs["linecolor"] if "linecolor" in kwargs else "C0"
        ndot = kwargs["ndot"] if "ndot" in kwargs else 1000
        ax.scatter(self.x, self.y - self.y_hat, s=s, c=c, label=label)
        x = np.linspace(self.x.min(), self.x.max(), ndot)
        ax.plot(x, np.zeros(x.size), c=lc, label="$y=0$")
        ax.set(xlabel="$Mean$", ylabel="Residual errors", title="Residual plot")
        ax.legend()


    def calibration_plot(
        self,
        ax: plt.Axes = None,
        hide_curve: bool = False,
        hide_dots: bool = False,
        label: str = None,
        linelabel: str = "LM",
        **kwargs
    ) -> None:
        super().calibration_plot(
            ax=ax,
            hide_curve=hide_curve,
            hide_dots=hide_dots,
            label=label,
            linelabel=linelabel,
            **kwargs
        )
