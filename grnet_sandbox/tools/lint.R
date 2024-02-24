### lint.R ###

suppressPackageStartupMessages({
  library(lintr)
})

dir_path <- "."

lint_dir(dir_path)
