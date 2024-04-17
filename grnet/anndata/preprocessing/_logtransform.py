from typing import Union

import numpy as np
from scipy.sparse import coo_matrix

from grnet.dev import ScipySparseMatrix, typechecker, valchecker


def logtransform(
    mtx: ScipySparseMatrix,
    base: Union[int, float] = np.e
) -> coo_matrix:
    typechecker(mtx, ScipySparseMatrix, "mtx")
    typechecker(base, (int, float), "base")
    log = {
        np.e: np.log,
        2: np.log2,
        10: np.log10
    }
    valchecker(base in log, f"Unsupported base number: {base}")
    return coo_matrix((log[base](mtx.data + 1), (mtx.row, mtx.col)), shape=mtx.shape)
