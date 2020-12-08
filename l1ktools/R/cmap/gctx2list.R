#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = T)
if(length(args) != 2) {
  stop("invalid number of arguments")
}

library(rhdf5)
library(data.table)
source("l1ktools/R/cmap/io.R")

batch <- 1000

cols <- read.gctx.ids(args[1], dimension = "col")

for(i in seq(1, length(cols), batch)) {
  end <- i + batch - 1
  if(end > length(cols)) {
    end <- length(cols)
  }
  ids <- cols[i:end]
  g <- parse.gctx(args[1], cid = ids)
  dt <- as.data.table(g@mat, keep.rownames = T)
  dt <- melt(dt, id.vars = "rn", variable.name = "sig_id", value.name = "zscore", na.rm = T)
  setnames(dt, "rn", "pr_gene_id")
  if(file.exists(args[2])) {
    fwrite(dt, file = args[2], append = T, sep = "\t", col.names = F, row.names = F, quote = F)
  } else {
    fwrite(dt, file = args[2], append = F, sep = "\t", col.names = T, row.names = F, quote = F)
  }
  rm(g)
  rm(dt)
  rm(ids)
  cat(end, " records saved\n")
}