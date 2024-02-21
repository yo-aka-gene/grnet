import argparse
import os

import anndata as ad
import scanpy as sc


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


args = parser.parse_args()
eval(f"sc.read_{args.format}")(args.input).write(args.output)