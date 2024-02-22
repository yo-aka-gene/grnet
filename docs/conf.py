# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import glob
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import grnet

project = 'Grnet'
copyright = '2023, Yuji Okano'
author = 'Yuji Okano'
version = grnet.__version__
release = grnet.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'nbsphinx', 'sphinx_gallery.load_style', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'grnet_doc'
html_logo = "_static/title.PNG"
html_theme_options = {"navigation_depth": 5, "logo_only": True, "sidebarbgcolor": "#003F67"}
master_doc = 'index'
latex_documents = [
    (master_doc, 'grnet.tex',
     'Grnet Documentation',
     'Yuji Okano', 'manual'),
]

man_pages = [
    (master_doc, 'grnet',
     'Grnet Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'grnet',
     'Grnet Documentation',
     author,
     'grnet',
     'Python package for gene regulatory networks (GRN) using Bayesian network',
     'Miscellaneous'),
]

nbsphinx_thumbnails = {
    "/".join(
        v.split(".")[:-1]
    ): v.replace(
        "notebooks", "_static"
    ).replace(
        "ipynb", "png"
    ) if os.path.exists(
        v.replace(
            "notebooks", "_static"
        ).replace(
            "ipynb", "png"
        )
    ) else "_static/logo.PNG" for v in glob.glob("notebooks/*")
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
