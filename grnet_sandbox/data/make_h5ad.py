import argparse
import os

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc

parser = argparse.ArgumentParser(
    description="Utility func to convert data to h5ad files"
)

parser.add_argument("-i", "--input", help="path of existing data path", required=True)

parser.add_argument("-o", "--output", help="path of existing data path", required=True)


parser.add_argument(
    "-f",
    "--format",
    help="path of existing data path",
    default="10x_mtx",
    required=False,
)


parser.add_argument(
    "-m",
    "--metadata",
    help="path of existing metadata path",
    default=None,
    required=False,
)


transpose = lambda fmt: ".T" if fmt in ["csv", "text"] else ""


args = parser.parse_args()
adata = eval(f"sc.read_{args.format}('{args.input}'){transpose(args.format)}")

if args.metadata is not None:
    fileformat = {
        "csv": {"suffix": "csv", "kwargs": {}},
        "text": {"suffix": "csv", "kwargs": {"sep": "\t"}},
    }

    source_suffix = (lambda d, a, k: d[a][k] if a in d else a)(
        fileformat, args.format, "suffix"
    )
    kwargs = (lambda d, a, k: d[a][k] if a in d else {})(
        fileformat, args.format, "kwargs"
    )

    adata.obs = eval(f"pd.read_{source_suffix}('{args.metadata}', **kwargs)")

adata.obs.index = pd.Index(np.array(adata.obs.index).astype(object), dtype=object)
adata.var.index = pd.Index(np.array(adata.var.index).astype(object), dtype=object)

for df in [adata.obs, adata.var]:
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) or "arrow" in str(df[col].dtype).lower():
            df[col] = df[col].to_numpy(dtype=object)

adata.write(args.output)
