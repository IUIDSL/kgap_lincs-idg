#!/bin/bash

cwd=$(pwd)

psql postgres < ${cwd}/sql/lincs/initdb.sql
psql lincs < ${cwd}/sql/lincs/tables.sql


${cwd}/l1ktools/R/cmap/gctx2list.R ~/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx ~/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.list.txt
${cwd}/l1ktools/R/cmap/gctx2list.R ~/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx ~/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.list.txt

${cwd}/R/gene.R ~/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_gene_info_2017-03-06.txt.gz ~/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_gene_info.txt.gz ~/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_gene_info_delta_landmark.txt.gz
${cwd}/R/cell.R
${cwd}/R/perturbagen.R
${cwd}/R/signature.R

psql lincs < ${cwd}/sql/lincs/import.sql
psql lincs < ${cwd}/sql/lincs/postimp.sql

# dcmap.sql output from gen.dcmap.R.
#psql lincs < ~/Documents/dbase/lincs/dcmap.sql
psql lincs < ${cwd}/sql/lincs/dcmap.sql
