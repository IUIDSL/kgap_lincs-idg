#!/usr/bin/env Rscript

library(data.table)

part1 <- fread(sprintf("gunzip -c %s/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_pert_info.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"), colClasses = c("character", "character", "character", "logical", "character", "character", "character", "character"))
part1[, `:=`(is_touchstone = NULL, inchi_key_prefix = NULL, pubchem_cid = NULL)]
part2 <- fread(sprintf("gunzip -c %s/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_pert_info_2017-03-06.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"))
part3 <- fread(sprintf("gunzip -c %s/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_pert_info.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"))
part3 <- part3[!pert_id %chin% part2[, pert_id]]

pert <- rbindlist(list(part1, part2, part3), use.names = T, fill = T)

pert <- unique(pert, by = "pert_id")
fwrite(pert, paste0(Sys.getenv("HOME"), "/Documents/dbase/lincs/perturbagen.tsv"), sep = "\t", col.names = T, row.names = F, quote = T, na = "NA")
