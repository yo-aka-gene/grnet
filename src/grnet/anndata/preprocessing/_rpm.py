from grnet.dev import ScipySparseMatrix, typechecker


def rpm(mtx: ScipySparseMatrix) -> ScipySparseMatrix:
    typechecker(mtx, ScipySparseMatrix, "mtx")
    return 1e6 * mtx / mtx.sum(axis=1)


def rp100k(mtx: ScipySparseMatrix) -> ScipySparseMatrix:
    typechecker(mtx, ScipySparseMatrix, "mtx")
    return 1e5 * mtx / mtx.sum(axis=1)
