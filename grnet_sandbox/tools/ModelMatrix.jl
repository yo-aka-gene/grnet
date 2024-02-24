module ModelMatrix
using PyCall

py"""
import sys
sys.path.insert(0, "./")
"""

const grnet = pyimport("grnet")
const ad = pyimport("anndata")

function 