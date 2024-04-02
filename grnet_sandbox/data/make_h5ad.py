import argparse
import os

import anndata as ad
import scanpy as sc
import pandas as pd


parser = argparse.ArgumentParser(
    description="Utility func to convert data to h5ad files"
)

parser.add_argument(
    "-i", "--input",
    help="path of existing data path",
    required=True
)

parser.add_argument(
    "-o", "--output",
    help="path of existing data path",
    required=True
)


parser.add_argument(
    "-f", "--format",
    help="path of existing data path",
    default="10x_mtx",
    required=False
)


parser.add_argument(
    "-m", "--metadata",
    help="path of existing metadata path",
    default=None,
    required=False
)


transpose = lambda fmt: ".T" if fmt in ["csv", "text"] else ""


args = parser.parse_args()
adata = eval(
    f"sc.read_{args.format}('{args.input}'){transpose(args.format)}"
)

if args.metadata is not None:
    fileformat = {
        "csv": {"suffix": "csv", "kwargs": {}},
        "text": {"suffix": "csv", "kwargs": {"sep": "\t"}}
    }
    
    source_suffix = (
        lambda d, a, k: d[a][k] if a in d else a
    )(fileformat, args.format, "suffix")
    kwargs = (
        lambda d, a, k: d[a][k] if a in d else {}
    )(fileformat, args.format, "kwargs")
    
    adata.obs = eval(
        f"pd.read_{source_suffix}('{args.metadata}', **kwargs)"
    )

adata.write(args.output)