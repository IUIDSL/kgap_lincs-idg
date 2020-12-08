#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = T)

if(length(args) == 0) {
  stop("At least one file argument required")
}

library(data.table)

genes <- data.table()

for(fn in args) {
  if(endsWith(fn, "landmark.txt.gz")) {
    dt <- fread(paste0("gunzip -c ", fn), header = T, sep = "\t", quote = "")
  	dt[, pr_is_lm := 1]
  } else {
  	dt <- fread(paste0("gunzip -c ", fn), header = T, sep = "\t", quote = "", select = c("pr_gene_id","pr_gene_symbol","pr_gene_title","pr_is_lm","pr_is_bing"))
  }
  genes <- rbindlist(list(genes, dt), use.names = T, fill = T)
}

genes <- unique(genes, by = "pr_gene_id")
fwrite(genes, paste0(Sys.getenv("HOME"), "/Documents/dbase/lincs/genes.tsv"), sep = "\t", col.names = T, row.names = F, quote = T, na = "NA")
