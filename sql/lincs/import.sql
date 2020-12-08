COPY level5(pr_gene_id, sig_id, zscore)
FROM PROGRAM 'gunzip -c /home/oleg/Documents/dbase/lincs/GSE70138/GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.list.txt.gz'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);

COPY level5(pr_gene_id, sig_id, zscore)
FROM PROGRAM 'gunzip -c /home/oleg/Documents/dbase/lincs/GSE92742/GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.list.txt.gz'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);


COPY gene(pr_gene_id, pr_gene_symbol, pr_gene_title,pr_is_lm,pr_is_bing)
FROM '/home/oleg/Documents/dbase/lincs/genes.tsv'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);

COPY instance(inst_id, cell_id, det_plate,det_well,pert_dose,pert_dose_unit,pert_id,pert_iname,pert_type,pert_time,pert_time_unit)
FROM '/home/oleg/Documents/dbase/lincs/instance.tsv'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);

COPY perturbagen(pert_id,pert_iname,pert_type,inchi_key,canonical_smiles)
FROM '/home/oleg/Documents/dbase/lincs/perturbagen.tsv'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);

COPY signature(sig_id,pert_id,pert_iname,pert_type,cell_id,pert_idose,pert_itime)
FROM '/home/oleg/Documents/dbase/lincs/signature.tsv'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);

COPY cell(cell_id,cell_type,cell_lineage,cell_histology,cell_source_id,cell_source,gender)
FROM '/home/oleg/Documents/dbase/lincs/cells.tsv'
WITH (
	FORMAT CSV,
	HEADER true,
	NULL 'NA',
	DELIMITER E'\t',
	QUOTE '"'
);
