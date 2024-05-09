from typing import Union

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix
from torch import Tensor

ScipySparseMatrix = Union[
    coo_matrix,
    csr_matrix,
    csc_matrix
]

AlgebraicArrays = Union[
    np.ndarray,
    Tensor
]
