#!/bin/bash

cwd=$(pwd)

SRCDATADIR="$HOME/../data/LINCS/data"
DATADIR=${cwd}/data
#
###
# L1K tools:
${cwd}/l1ktools/R/cmap/gctx2list.R \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.list.txt
#
${cwd}/l1ktools/R/cmap/gctx2list.R \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.list.txt
###
# Custom code:
${cwd}/python/gene.py \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_gene_info_2017-03-06.txt.gz \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_gene_info.txt.gz \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_gene_info_delta_landmark.txt.gz
#
${cwd}/python/cell.py \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_cell_info_2017-04-28.txt.gz \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_cell_info.txt.gz \
	$DATADIR/cells.tsv
#
${cwd}/python/perturbagen.py \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_pert_info.txt.gz \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_pert_info_2017-03-06.txt.gz \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_pert_info.txt.gz \
	$DATADIR/perturbagen.tsv
#
${cwd}/python/signature.py \
	$SRCDATADIR/GSE70138/GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz \
	$SRCDATADIR/GSE92742/GSE92742_Broad_LINCS_sig_info.txt.gz \
	$DATADIR/signature.tsv
#
###
# Create database
psql postgres <${cwd}/sql/lincs/initdb.sql
psql lincs <${cwd}/sql/lincs/tables.sql
#
psql lincs <${cwd}/sql/lincs/import.sql
psql lincs <${cwd}/sql/lincs/postimp.sql
#
###
# Map drugs by structure.
${cwd}/python/dcmap.py ${DATADIR}/dcmap.sql
psql lincs< ${DATADIR}/dcmap.sql
#
