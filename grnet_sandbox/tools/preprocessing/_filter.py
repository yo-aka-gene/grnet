from typing import Callable, Dict
import anndata as ad
import numpy as np


def get_quantiles(
    data: ad.AnnData, 
    metrics: str, 
    by: float = .1,
    area: list = None
):
    area = np.arange(0, 1, by)[1:] if area is None else area
    return [
        data.obs[metrics].quantile(v) for v in area
    ]


def filter_pipeline(
    data: ad.AnnData,
    filter_dict: Dict[str, Callable],
    return_adata: bool = True
) -> ad.AnnData:
    for kind, func in filter_dict.items():
        data = data[func(data.obs[kind]), :]
    return data if return_adata else None
