#!/usr/bin/env Rscript

library(data.table)

if(length(args) < 3) {
  stop("3 file args required, 2 input, 1 output.")
}

fn1 <- args[1] #GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz
fn2 <- args[2] #GSE92742_Broad_LINCS_sig_info.txt.gz
ofile <- args[3] #signature.tsv
#
part1 <- fread(sprintf("gunzip -c %s", fn1), header=T, sep="\t",
quote="", na.strings=c("NA", "", "", "-666", "-666.0"))
part1 <- part1[, .(sig_id,pert_id,pert_iname,pert_type,cell_id,pert_idose,pert_itime)]
#
part2 <- fread(sprintf("gunzip -c %s", fn2), header=T, sep="\t",
quote="", na.strings=c("NA", "", "", "-666", "-666.0"), colClasses=c("character", "character", "character", "character", "character", "character", "character", "character", "integer", "character", "character", "character"))
part2 <- part2[, .(sig_id,pert_id,pert_iname,pert_type,cell_id,pert_idose,pert_itime)]
#
sign <- rbindlist(list(part1, part2), use.names=T, fill=T)
sign <- unique(sign, by="sig_id")
fwrite(sign, ofile, sep="\t", col.names=T, row.names=F, quote=T, na="NA")
