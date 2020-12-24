#!/usr/bin/env Rscript

library(data.table)

if(length(args) < 4) {
  stop("4 args required, 3 input files, 1 output.")
}

fn1 <- args[1] #GSE92742_Broad_LINCS_pert_info.txt.gz
fn2 <- args[2] #GSE70138_Broad_LINCS_pert_info_2017-03-06.txt.gz
fn3 <- args[3] #GSE70138_Broad_LINCS_pert_info.txt.gz
ofile <- args[4] #perturbagen.tsv
#
part1 <- fread(sprintf("gunzip -c %s", fn1), header=T, sep="\t",
quote="", na.strings=c("NA", "", "", "-666", "-666.0"), colClasses=c("character", "character", "character", "logical", "character", "character", "character", "character"))
part1[, `:=`(is_touchstone=NULL, inchi_key_prefix=NULL, pubchem_cid=NULL)]
#
part2 <- fread(sprintf("gunzip -c %s", fn2), header=T, sep="\t",
quote="", na.strings=c("NA", "", "", "-666", "-666.0"))
#
part3 <- fread(sprintf("gunzip -c %s", fn3), header=T, sep="\t",
quote="", na.strings=c("NA", "", "", "-666", "-666.0"))
part3 <- part3[!pert_id %chin% part2[, pert_id]]
#
pert <- rbindlist(list(part1, part2, part3), use.names=T, fill=T)
pert <- unique(pert, by="pert_id")
fwrite(pert, ofile, sep="\t", col.names=T, row.names=F, quote=T, na="NA")
