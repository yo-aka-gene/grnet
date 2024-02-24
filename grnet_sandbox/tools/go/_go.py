import os
import subprocess
from tempfile import TemporaryDirectory

import anndata as ad
import matplotlib.pyplot as plt
from mygene import MyGeneInfo
import numpy as np
import pandas as pd
import polars as pl
import seaborn as sns


def term_array(
    symbol: str,
    species: str = "mouse"
) -> np.ndarray:
    arr = np.concatenate([
        [vv["term"] for vv in v] for v in MyGeneInfo().query(
            symbol, scopes="symbol", fields="go", species=species
        )["hits"][0]["go"].values()
    ])
    _, idx = np.unique(arr, return_index=True)
    return arr[np.sort(idx)]


def gprofiler(data: np.ndarray) -> pd.DataFrame:
    tempdir = TemporaryDirectory()
    pl.from_numpy(data, schema=["symbols"]).write_ipc(f"{tempdir.name}/data.feather")
    cmd = f"Rscript {os.path.dirname(__file__)}/go_pipeline.R -t {tempdir.name}"
    subprocess.call(cmd.split())
    ret = pl.read_ipc(f"{tempdir.name}/enrichment.feather").to_pandas()
    tempdir.cleanup()
    return ret


def get_deg(
    data: ad.AnnData,
    cluster_name: str,
    pvals_adj: float = .05,
    max_logfc: float = np.inf,
    min_logfc: float = -np.inf
) -> np.ndarray:
    loc = (
        data.uns["rank_genes_groups"]["pvals_adj"][cluster_name] < pvals_adj
    ) & (
        data.uns["rank_genes_groups"]["logfoldchanges"][cluster_name] < max_logfc
    ) & (
        data.uns["rank_genes_groups"]["logfoldchanges"][cluster_name] > min_logfc
    )
    return data.uns["rank_genes_groups"]["names"][cluster_name][loc]


def top_degs(
    data: ad.AnnData,
    top: int = 5,
    pvals_adj: float = .05,
    max_logfc: float = np.inf,
    min_logfc: float = -np.inf,
    unique: bool = True
) -> np.ndarray:
    arr = np.concatenate(
        [
            get_deg(
                data=data,
                cluster_name=name,
                pvals_adj=pvals_adj,
                max_logfc=max_logfc,
                min_logfc=min_logfc
            )[:top] for name in data.uns["rank_genes_groups"]["names"].dtype.names
        ],
        axis=0
    )
    _, idx = np.unique(arr, return_index=True)
    return arr[np.sort(idx)] if unique else arr


def go_plot(
    data: ad.AnnData,
    cluster_name: str,
    pvals_adj: float = .05,
    max_logfc: float = np.inf,
    min_logfc: float = -np.inf,
    ax: plt.Axes = None,
    top: int = None,
    palette: str = None
) -> plt.Axes:
    top = 100000 if top is None else top
    genes = get_deg(
        data=data,
        cluster_name=cluster_name,
        pvals_adj=pvals_adj,
        max_logfc=max_logfc,
        min_logfc=min_logfc
    )

    if genes.size <= 1:
        terms = term_array(
            genes[0]
        )[:top][::-1] if genes.size == 1 else None
        res = pd.DataFrame({
            "term_name": terms,
            "p_value": np.array([np.nan] * terms.size),
            "intersection_size": np.array([np.nan] * terms.size),
            "term_size": np.ones(terms.size)
        }) if genes.size == 1 else None

    else:
        res = gprofiler(
            genes
        ).iloc[:top, :].iloc[::-1, :]

    if ax is None and genes.size != 0:
        ysize = (lambda x: max(5, int(x / 5)))(min(top, len(res)))
        _, ax = plt.subplots(figsize=(5, ysize))

    if genes.size >= 1:
        res = pd.DataFrame({
            "term_name": res.term_name,
            "$-\log_{10}P$": -np.log10(res.p_value),
            "Intersection size": res.intersection_size,
            "gene_ratio": res.intersection_size / res.term_size
        })

        sns.scatterplot(
            data=res,
            x="gene_ratio",
            y="term_name",
            size="Intersection size",
            hue="$-\log_{10}P$",
            palette=palette if genes.size > 1 else None,
            ax=ax,
            **{"edgecolor": ".2", "linewidth": .5}
        )

        ax.set_ylim(-.5, min(len(res), top) - .5)
        ax.set(ylabel="", xlabel="Gene Ratio")
        ax.legend(
            loc="center left",
            bbox_to_anchor=(1, .5)
        ) if genes.size > 1 else ax.text(
            .5, np.mean(ax.get_ylim()), "N/A\n" + f"(DEG: {genes[0]})",
            ha="center", va="center"
        )
        return ax


def rename_by_top_sigup(
    data: ad.AnnData,
    pvals_adj: float = .05,
    min_logfc: float = -np.inf,
) -> np.ndarray:
    arr = [
        get_deg(
            data=data,
            cluster_name=name,
            pvals_adj=pvals_adj,
            min_logfc=min_logfc
        ) for name in data.uns["rank_genes_groups"]["names"].dtype.names
    ]
    arr = np.array([
        f"{v[0]}+" if v.size != 0 else "Unknown" for v in arr
    ])

    unique, inverse, counts = np.unique(
        arr,
        return_inverse=True,
        return_counts=True
    )

    ret = []
    for i, v in enumerate(arr):
        if counts[np.where(unique == v)].item() == 1:
            ret += [v]
        else:
            unique_id = np.where(unique == v)[0].item()
            duplicates_loc = np.arange(arr.size)[inverse == unique_id]
            suffix = np.where(duplicates_loc == i)[0].item() + 1
            ret += [f"{v}({suffix})"]

    return np.array(ret)


def _tally_util(
    df: pd.DataFrame,
    groupby: str,
    x: str,
    stack: bool = False
):
    df = df.value_counts()
    df.name = "counts"
    df = pd.DataFrame(df).reset_index()

    def fmt_df(
        d: pd.DataFrame
    ) -> pd.DataFrame:
        return d.assign(
            Proportion=d.counts.cumsum() / d.counts.sum()
        ) if stack else d.assign(
            Proportion=d.counts / d.counts.sum()
        )

    df = pd.concat(
        [
            fmt_df(df[(df[x] == dn)].sort_values(groupby)) for dn in np.sort(
                df[x].unique()
            )
        ],
        axis=0
    )
    return df


def tally(
    data: ad.AnnData,
    groupby: str,
    x: str = "batch"
):
    return _tally_util(
        data.obs[[x, groupby]],
        x=x, groupby=groupby
    )


def stacked_tally(
    data,
    groupby: str,
    x: str = "batch"
):
    return _tally_util(
        data.obs[[x, groupby]],
        x=x, groupby=groupby,
        stack=True
    )


def merged_tally(
    data: ad.AnnData,
    merge_list: list,
    new_name: str,
    groupby: str,
    x: str = "batch"
):
    obs = [x, groupby]
    for i, target in enumerate(merge_list):
        if i == 0:
            loc = (data.obs[obs] == target)
        else:
            loc |= (data.obs[obs] == target)
    df = pd.DataFrame(
        np.where(loc, new_name, data.obs[obs]),
        index=data.obs.index,
        columns=obs
    )
    return _tally_util(
        df=df, x=x, groupby=groupby
    )