from typing import Callable

import anndata as ad
import numpy as np

from grnet.dev import typechecker


def binarize(
    data: ad.AnnData,
    normalizer: Callable = None,
    write: str = None
) -> ad.AnnData:
    typechecker(data, ad.AnnData, "data")
    if normalizer is not None:
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
    if write is not None:
        ret.write(write)
    return ret
