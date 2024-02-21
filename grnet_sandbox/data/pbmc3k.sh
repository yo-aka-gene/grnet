#!/bin/sh

DATA_DIR=/home/jovyan/data

wget http://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz -O $DATA_DIR/pbmc3k.tar.gz
cd $DATA_DIR; tar -xzf pbmc3k.tar.gz
gzip -d *.gz
python /home/jovyan/data/make_h5ad.py -i "/home/jovyan/data/filtered_gene_bc_matrices/hg19" -o "/home/jovyan/data/pbmc3k.h5ad"
rm -rf *.tar
rm -rf /home/jovyan/data/filtered_gene_bc_matrices