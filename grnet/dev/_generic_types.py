from typing import Union

from scipy.sparse import coo_matrix, csr_matrix, csc_matrix

ScipySparseMatrix = Union[
    coo_matrix,
    csr_matrix,
    csc_matrix
]
