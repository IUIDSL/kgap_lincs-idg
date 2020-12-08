create table if not exists level5(
	pr_gene_id integer not null,
	sig_id varchar(50) not null,
	zscore double precision not null,
	primary key(pr_gene_id, sig_id)
);

create table if not exists level5_lm(
	pr_gene_id integer not null,
	sig_id varchar(50) not null,
	zscore double precision not null,
	primary key(pr_gene_id, sig_id)
);

create table if not exists gene(
	pr_gene_id integer primary key,
	pr_gene_symbol varchar(20),
	pr_gene_title varchar(200),
	pr_is_lm smallint not null,
	pr_is_bing smallint
);

create table if not exists perturbagen(
	pert_id varchar(30) primary key,
	pert_iname varchar(200),
	pert_type varchar(20),
	inchi_key char(27),
	canonical_smiles varchar(4000)
);

create table if not exists signature(
	sig_id varchar(50) primary key,
	pert_id varchar(30) not null,
	pert_iname varchar(200),
	pert_type varchar(20),
	cell_id varchar(10) not null,
	pert_idose varchar(20),
	pert_itime varchar(20)
);

create table if not exists cell(
	cell_id varchar(10) primary key,
	cell_type varchar(20),
	cell_lineage varchar(50),
	cell_histology varchar(100),
	cell_source_id varchar(20),
	cell_source varchar(20),
	gender char(1) check (gender in ('M', 'F'))
);
