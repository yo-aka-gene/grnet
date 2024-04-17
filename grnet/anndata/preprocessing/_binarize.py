from typing import Callable

import anndata as ad
import numpy as np

from grnet.dev import typechecker


def binarize(
    data: ad.AnnData,
    normalizer: Callable = None
) -> ad.AnnData:
    typechecker(data, ad.AnnData, "data")
    typechecker(normalizer, Callable, "normalizer")
    ret = data.copy()
    ret.X = (ret.X != 0)
    ret.var["coverage"] = np.ravel(
        ret.X.sum(axis=0) / ret.shape[0]
    )
    ret.var["DOR"] = 1 - ret.var["coverage"]
    ret.var["Mean"] = np.ravel(
        data.X.mean(axis=0)
    ) if normalizer is None else np.ravel(
        normalizer(data.X).mean(axis=0)
    )
    ret.uns["binarized"] = True
    return ret
