#!/bin/sh

DATA_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPT_NAME=$(basename "$0" .sh)

curl -o "$DATA_DIR/matrix.tsv.gz"  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE133nnn/GSE133536/suppl/GSE133536%5F10X8x10Kcell25Kreads%5Fhuman%5Fexp%5Fmat.tsv.gz
curl -o "$DATA_DIR/meta.tsv.gz" https://ftp.ncbi.nlm.nih.gov/geo/series/GSE133nnn/GSE133536/suppl/GSE133536%5F10X8x10Kcell25Kreads%5Fhuman%5Fmetada.tsv.gz
gzip -d "$DATA_DIR"/*.gz
python "$DATA_DIR/10x80kc25kr.py" -i "$DATA_DIR/matrix.tsv" -o "$DATA_DIR/$SCRIPT_NAME.h5ad" -m "$DATA_DIR/meta.tsv"
rm -f "$DATA_DIR"/*.tsv