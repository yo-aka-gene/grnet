"""
Top level package of Grnet
"""

from . import (
    abstract,
    anndata,
    clusters,
    dev,
    evaluations,
    gene_selection,
    models,
    plot,
    toydata,
)

__all__ = [
    "abstract",
    "anndata",
    "clusters",
    "dev",
    "evaluations",
    "gene_selection",
    "models",
    "plot",
    "toydata",
]

__author__ = """Yuji Okano"""
__email__ = "yujiokano@keio.jp"
__version__ = "0.1.0"
