#!/usr/bin/env Rscript

library(data.table)

part1 <- fread(sprintf("gunzip -c %s/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"))
part1 <- part1[, .(sig_id,pert_id,pert_iname,pert_type,cell_id,pert_idose,pert_itime)]
part2 <- fread(sprintf("gunzip -c %s/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_sig_info.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"), colClasses = c("character", "character", "character", "character", "character", "character", "character", "character", "integer", "character", "character", "character"))
part2 <- part2[, .(sig_id,pert_id,pert_iname,pert_type,cell_id,pert_idose,pert_itime)]

sign <- rbindlist(list(part1, part2), use.names = T, fill = T)

sign <- unique(sign, by = "sig_id")
fwrite(sign, paste0(Sys.getenv("HOME"), "/Documents/dbase/lincs/signature.tsv"), sep = "\t", col.names = T, row.names = F, quote = T, na = "NA")
