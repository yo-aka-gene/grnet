import argparse
import os

import anndata as ad
import pandas as pd
import scanpy as sc

parser = argparse.ArgumentParser(
    description="Utility func to convert data to h5ad files"
)

parser.add_argument("-i", "--input", help="path of existing data path", required=True)

parser.add_argument("-o", "--output", help="path of existing data path", required=True)

parser.add_argument(
    "-m", "--metadata", help="path of existing metadata path", required=True
)


args = parser.parse_args()
adata = sc.read_text(args.input, dtype="int16").T
adata.obs = pd.read_csv(args.metadata, sep="\t")

adata.write(args.output)
