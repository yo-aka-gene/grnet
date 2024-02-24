### set_renv.R ###

if (!requireNamespace("renv", quietly = TRUE)) {
  install.packages("renv", repos = "http://cran.ism.ac.jp/")
}