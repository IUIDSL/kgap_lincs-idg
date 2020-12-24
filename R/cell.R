#!/usr/bin/env Rscript

library(data.table)

args <- commandArgs(trailingOnly = T)

if(length(args) < 2) {
  stop("3 file args required, LINCS cell info for GSE70138 and GSE92742, and output file.")
}

fn1 <- args[1]
fn2 <- args[2]
ofile <- args[3]

cells <- data.table()

GSE70138 <- fread(paste0("gunzip -c ", fn1), header=T, sep="\t", quote="", na.strings="-666")

setnames(GSE70138, "donor_sex", "gender")
setnames(GSE70138, "primary_site", "cell_lineage")
setnames(GSE70138, "subtype", "cell_histology")
setnames(GSE70138, "provider_catalog_id", "cell_source_id")
setnames(GSE70138, "original_source_vendor", "cell_source")

GSE70138 <- GSE70138[, .(cell_id, cell_type, cell_lineage, cell_histology, cell_source_id, cell_source, gender)]

#
GSE92742 <- fread(paste0("gunzip -c ", fn2), header=T, sep="\t", quote="", na.strings="-666")

setnames(GSE92742, "donor_sex", "gender")
setnames(GSE92742, "primary_site", "cell_lineage")
setnames(GSE92742, "subtype", "cell_histology")
setnames(GSE92742, "provider_catalog_id", "cell_source_id")
setnames(GSE92742, "original_source_vendor", "cell_source")

GSE92742 <- GSE92742[, .(cell_id, cell_type, cell_lineage, cell_histology, cell_source_id, cell_source, gender)]

#
cells <- rbindlist(list(GSE70138, GSE92742), use.names=T, fill=T)
cells <- unique(cells, by = "cell_id")
fwrite(cells, ofile, sep="\t", col.names=T, row.names=F, quote=T, na="NA")
