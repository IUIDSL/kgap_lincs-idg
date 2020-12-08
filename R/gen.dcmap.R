#!/usr/bin/env Rscript

library(RJDBC)
library(data.table)

out.fn <- paste0(Sys.getenv("HOME"), "/Documents/dbase/lincs/dcmap.sql")

cat("update perturbagen set dc_id = null, is_parent = null;", file = out.fn, sep = "\n")

drv <-
JDBC("org.apache.derby.jdbc.EmbeddedDriver",paste0(Sys.getenv("HOME"), "/app/db-derby-10.14.1.0-bin/lib/derby.jar"), identifier.quote="\"")
conn <- dbConnect(drv, paste0("jdbc:derby:", Sys.getenv("HOME"), "/Documents/dbase/drugdb/.config/localdb/db"))
drug.names <- dbGetQuery(conn, "select id,name,parent_id from synonyms")
setDT(drug.names)
drug.inchi <- dbGetQuery(conn, "select id,inchikey from structures where inchikey is not null")
setDT(drug.inchi)
parent.inchi <- dbGetQuery(conn, "select CD_ID ID,inchikey from parentmol where inchikey is not null")
setDT(parent.inchi)
dbDisconnect(conn)
dbUnloadDriver(drv)
rm(conn)
rm(drv)

drug.names[NAME %like% "'", NAME := gsub("'","''",NAME,fixed = T)]

d1 <- drug.names[!is.na(ID)]
d1[, sql := sprintf("update perturbagen set dc_id = %d where lower('%s')=lower(pert_iname) and pert_type = 'trt_cp';", ID, NAME)]
cat(d1$sql, file = out.fn, sep = "\n", append = T)

d2 <- drug.names[is.na(ID) & !is.na(PARENT_ID)]
d2[, sql := sprintf("update perturbagen set dc_id = %d,is_parent=true where lower('%s')=lower(pert_iname) and pert_type = 'trt_cp' and dc_id is null;", PARENT_ID, NAME)]
cat(d2$sql, file = out.fn, sep = "\n", append = T)


drug.inchi[, sql := sprintf("update perturbagen set dc_id = %d where inchi_key='%s' and pert_type = 'trt_cp' and dc_id is null;", ID, INCHIKEY)]
cat(drug.inchi$sql, file = out.fn, sep = "\n", append = T)

parent.inchi[, sql := sprintf("update perturbagen set dc_id = %d,is_parent=true where inchi_key='%s' and pert_type = 'trt_cp' and dc_id is null;", ID, INCHIKEY)]
cat(parent.inchi$sql, file = out.fn, sep = "\n", append = T)

cat("create index pert_drug_idx on perturbagen(dc_id);", file = out.fn, sep = "\n", append = T)
