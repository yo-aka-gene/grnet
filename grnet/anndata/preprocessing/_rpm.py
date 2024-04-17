from scipy.sparse import coo_matrix

from grnet.dev import typechecker


def rpm(mtx: coo_matrix) -> coo_matrix:
    typechecker(mtx, coo_matrix, "mtx")
    return 1e6 * mtx / mtx.sum(axis=1)


def rp100k(mtx: coo_matrix) -> coo_matrix:
    typechecker(mtx, coo_matrix, "mtx")
    return 1e5 * mtx / mtx.sum(axis=1)
