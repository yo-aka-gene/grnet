from pathlib import Path

import matplotlib as mpl

mpl.rcParams.update(
    {
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


kwarg_savefig = {
    "facecolor": "white",
    "dpi": 600,
    "bbox_inches": "tight",
    "pad_inches": 0.05,
    "transparent": True,
}


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

dsname = {
    "10x10kc250kr": "Chromium V2\n(deep)",
    "10x80kc25kr": "Chromium V2\n(shallow)",
    "singlenuclei": "Chromium V2\n(sn)",
    "10xv3": "Chromium V3",
    "c1htmedium": "C1HT-medium",
    "c1htsmall": "C1HT-small",
    "celseq2": "CEL-seq2",
    "dropseq": "Drop-seq",
    "icell8": "ICELL8",
    "marsseq": "MARS-Seq",
    "quartzseq2": "Quartz-Seq2",
    "gmcscrbseq": "gmcSCRB-seq",
    "ddseq": "ddSEQ",
    "indrop": "inDrop",
    "smartseq2": "Smart-Seq2",
}
