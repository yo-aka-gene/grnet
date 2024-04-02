#!/bin/sh

DATA_DIR=/home/jovyan/data

curl -o $DATA_DIR/matrix.tsv.gz https://ftp.ncbi.nlm.nih.gov/geo/series/GSE141nnn/GSE141469/suppl/GSE141469%5F10XV3%5Fhuman%5Fexp%5Fmat.tsv.gz
curl -o $DATA_DIR/meta.tsv.gz https://ftp.ncbi.nlm.nih.gov/geo/series/GSE141nnn/GSE141469/suppl/GSE141469%5F10XV3%5Fhuman%5Fmetadata.tsv.gz
cd $DATA_DIR; gzip -d *.gz
python /home/jovyan/data/make_h5ad.py -i "/home/jovyan/data/matrix.tsv" -o "/home/jovyan/data/10xv3.h5ad" -f "text" -m "/home/jovyan/data/meta.tsv"
rm -rf /home/jovyan/data/*.tsv