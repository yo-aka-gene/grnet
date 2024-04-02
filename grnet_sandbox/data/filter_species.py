import argparse
import os

import scanpy as sc


parser = argparse.ArgumentParser(
    description="Utility func to extract specific species from h5ad files"
)

parser.add_argument(
    "-d", "--data",
    help="path of existing data path",
    required=True
)

parser.add_argument(
    "-s", "--species",
    help="name of species to extract",
    required=True
)

args = parser.parse_args()
adata = sc.read_h5ad(args.data)
adata[adata.obs["Species"] == args.species, :].write(args.data)
