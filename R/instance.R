#!/usr/bin/env Rscript

library(data.table)

part1 <- fread(sprintf("gunzip -c %s/../data/LINCS/data/GSE70138/GSE70138_Broad_LINCS_inst_info_2017-03-06.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"))
part1 <- part1[, .(inst_id, cell_id, det_plate, det_well, pert_dose, pert_dose_unit, pert_id, pert_iname, pert_type, pert_time, pert_time_unit)]
part2 <- fread(sprintf("gunzip -c %s/../data/LINCS/data/GSE92742/GSE92742_Broad_LINCS_inst_info.txt.gz", Sys.getenv("HOME")), header = T, sep = "\t", quote = "", na.strings = c("NA", "", "", "-666", "-666.0"))
setnames(part2, "rna_plate", "det_plate")
setnames(part2, "rna_well", "det_well")
part2 <- part2[, .(inst_id, cell_id, det_plate, det_well, pert_dose, pert_dose_unit, pert_id, pert_iname, pert_type, pert_time, pert_time_unit)]

inst <- rbindlist(list(part1, part2), use.names = T, fill = T)

inst <- unique(inst, by = "inst_id")
fwrite(inst, "instance.tsv"), sep = "\t", col.names = T, row.names = F, quote = T, na = "NA")
