#!/bin/sh

DATA_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPT_NAME=$(basename "$0" .sh)

wget http://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz -O "$DATA_DIR/$SCRIPT_NAME.tar.gz"
tar -xzf "$DATA_DIR/$SCRIPT_NAME.tar.gz"
gzip -d "$DATA_DIR"/*.gz
python "$DATA_DIR/make_h5ad.py" -i "$DATA_DIR/filtered_gene_bc_matrices/hg19" -o "$DATA_DIR/$SCRIPT_NAME.h5ad"
rm -f "$DATA_DIR"/*.tar
rm -rf "$DATA_DIR/filtered_gene_bc_matrices"