import anndata as ad
import matplotlib.pyplot as plt
import numpy as np
import optuna
import statsmodels.api as sm

from grnet.anndata.preprocessing import binarize
from grnet.dev import Numeric64, typechecker
from sklearn.metrics import mean_squared_error

from ._abstract import DORModel


class GLM(DORModel):
    def __init__(
        self,
        family: str,
        link: str,
        random_state: int = 0,
        n_trials: int = 200,
        add_const: bool = True
    ) -> None:
        super().__init__(
            random_state=random_state,
            n_trials=n_trials
        )
        typechecker(add_const, bool, "add_const")
        self.family = eval(f"sm.families.{family}")
        self.link = eval(f"sm.genmod.families.links.{link}()")
        self.add_const = add_const


    def fit(
        self,
        data: ad.AnnData,
        **kwargs
    ) -> None:
        super().fit(data=data)
        self.y = data.var["DOR"].values
        self.x = data.var["Mean"].values
        result = sm.GLM(
            endog=self.y,
            exog=sm.add_constant(self.x) if self.add_const else self.x,
            family=self.family(link=self.link, **kwargs)
        ).fit()
        self.model = result
        self.params = result.params
        self.f = lambda mean: result.predict(sm.add_constant(mean) if self.add_const else mean)
        self.y_hat = self.f(self.x)
        self.mse = mean_squared_error(self.y, self.y_hat)
        y_intercep, coeff = result.params
        self.predict_mean = lambda dor: ((np.log(dor) - y_intercep) / coeff)


    def calibration_plot(
        self,
        ax: plt.Axes = None,
        hide_curve: bool = False,
        hide_dots: bool = False,
        label: str = None,
        linelabel: str = "GLM",
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


class NegativeBinomial(GLM):
    def __init__(
        self,
        random_state: int = 0,
        n_trials: int = 200,
        add_const: bool = True,
        verbosity: str = "CRITICAL",
        search_min: Numeric64 = .01,
        search_max: Numeric64 = 2,
    ) -> None:
        super().__init__(
            family="NegativeBinomial",
            link="Log",
            random_state=random_state,
            n_trials=n_trials,
            add_const=add_const
        )
        self.verbosity = eval(f"optuna.logging.{verbosity}")
        typechecker(search_min, Numeric64, "search_min")
        typechecker(search_max, Numeric64, "search_max")
        self.search_range = (search_min, search_max)



    def optimize_alpha(
            self,
            data: ad.AnnData
        ) -> Numeric64:
        typechecker(data, ad.AnnData, "data")
        data = binarize(data) if "binarized" not in data.uns else data
        y = data.var["DOR"].values
        X = sm.add_constant(
            data.var["Mean"].values
        ) if self.add_const else data.var["Mean"].values
        optuna.logging.set_verbosity(self.verbosity)

        def objective(trial):
            alpha = trial.suggest_float('alpha', *self.search_range)
            nb = sm.GLM(endog=y, exog=X, family=self.family(alpha=alpha, link=self.link))
            return nb.fit().aic

        study = optuna.create_study(
            direction='minimize', 
            sampler=optuna.samplers.TPESampler(seed=self.seed)
        )
        study.optimize(objective, n_trials=self.n_trials)
        return study.best_params['alpha']


    def fit(
        self,
        data: ad.AnnData
    ) -> None:
        typechecker(data, ad.AnnData, "data")
        data = binarize(data) if "binarized" not in data.uns else data
        super().fit(data=data, alpha=self.optimize_alpha(data=data))


    def calibration_plot(
        self,
        ax: plt.Axes = None,
        hide_curve: bool = False,
        hide_dots: bool = False,
        label: str = None,
        linelabel: str = "NB",
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


class Poisson(GLM):
    def __init__(
        self,
        random_state: int = 0,
        n_trials: int = 200,
        add_const: bool = True
    ) -> None:
        super().__init__(
            family="Poisson",
            link="Log",
            random_state=random_state,
            n_trials=n_trials,
            add_const=add_const
        )


    def fit(
        self,
        data: ad.AnnData
    ) -> None:
        typechecker(data, ad.AnnData, "data")
        data = binarize(data) if "binarized" not in data.uns else data
        super().fit(data=data)


    def calibration_plot(
        self,
        ax: plt.Axes = None,
        hide_curve: bool = False,
        hide_dots: bool = False,
        label: str = None,
        linelabel: str = "Poisson",
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
