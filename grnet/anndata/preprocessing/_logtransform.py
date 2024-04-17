from typing import Union

import numpy as np
from scipy.sparse import coo_matrix

from grnet.dev import typechecker, valchecker


def logtransform(
    mtx: coo_matrix,
    base: Union[int, float] = np.e
) -> coo_matrix:
    typechecker(mtx, coo_matrix, "mtx")
    typechecker(base, (int, float), "base")
    log = {
        np.e: np.log,
        2: np.log2,
        10: np.log10
    }
    valchecker(base in log, f"Unsupported base number: {base}")
    return coo_matrix((log[base](mtx.data + 1), (mtx.row, mtx.col)), shape=mtx.shape)
