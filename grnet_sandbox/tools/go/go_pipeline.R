### go_pipeline.R ###

suppressPackageStartupMessages({
  library(optparse)
  library(arrow)
  library(gprofiler2)
})

optslist <- list(
  make_option(
    c("-t", "--tempdir"),
    typ = "character",
    default = "/home/jovyan/out",
    help = "temporary directory to save intermediate files"
  )
)
parser <- OptionParser(option_list = optslist)
opts <- parse_args(parser)

gene_loader <- function(path) {
  stopifnot(is.character(path))
  return(read_feather(path)$symbols)
}

egost <- function(
  gene,
  organism = "hsapiens",
  correction_method = "fdr",
  user_threshold = 0.05,
  domain_scope = "annotated",
  sources = "GO"
) {
  stopifnot(is.vector(gene))
  stopifnot(is.character(gene))
  stopifnot(is.character(organism))
  stopifnot(is.character(correction_method))
  stopifnot(is.numeric(user_threshold))
  return(
    gost(
      query = gene,
      organism = organism,
      correction_method = correction_method,
      user_threshold = user_threshold,
      domain_scope = domain_scope,
      sources = sources
    )
  )
}

go_result <- egost(gene = gene_loader(paste0(opts$tempdir, "/data.feather")))

write_feather(
  as.data.frame(go_result$result[, 1:13]),
  paste0(opts$tempdir, "/enrichment.feather")
)
