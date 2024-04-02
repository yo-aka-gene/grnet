#!/bin/sh

DATA_DIR=/home/jovyan/data

curl -o $DATA_DIR/matrix.tsv.gz https://ftp.ncbi.nlm.nih.gov/geo/series/GSE133nnn/GSE133536/suppl/GSE133536%5F10X8x10Kcell25Kreads%5Fhuman%5Fexp%5Fmat.tsv.gz
curl -o $DATA_DIR/meta.tsv.gz https://ftp.ncbi.nlm.nih.gov/geo/series/GSE133nnn/GSE133536/suppl/GSE133536%5F10X8x10Kcell25Kreads%5Fhuman%5Fmetada.tsv.gz
cd $DATA_DIR; gzip -d *.gz
python /home/jovyan/data/10x80kc25kr.py -i "/home/jovyan/data/matrix.tsv" -o "/home/jovyan/data/10x80kc25kr.h5ad" -m "/home/jovyan/data/meta.tsv"
rm -rf /home/jovyan/data/*.tsv