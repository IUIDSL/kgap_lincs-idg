// primary id
CREATE CONSTRAINT ON (n:Cell) ASSERT n.id IS UNIQUE;
CREATE CONSTRAINT ON (n:Concept) ASSERT n.id IS UNIQUE;
CREATE CONSTRAINT ON (n:Drug) ASSERT n.id IS UNIQUE;
CREATE CONSTRAINT ON (n:Gene) ASSERT n.id IS UNIQUE;
CREATE CONSTRAINT ON (n:Signature) ASSERT n.id IS UNIQUE;

// additional identifiers we want to be unique 
CREATE CONSTRAINT ON (n:Cell) ASSERT n.cell_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Concept) ASSERT n.omop_concept_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Drug) ASSERT n.dc_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Gene) ASSERT n.pr_gene_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Gene) ASSERT n.pr_gene_symbol IS UNIQUE;
CREATE CONSTRAINT ON (n:Signature) ASSERT n.sig_id IS UNIQUE;

// index commonly searched properties
CREATE INDEX FOR (n:Cell) ON (n.cell_histology);
CREATE INDEX FOR (n:Drug) ON (n.pert_iname);
CREATE INDEX FOR (n:Drug) ON (n.pert_type);
CREATE INDEX FOR (n:Gene) ON (n.pr_gene_title);
CREATE INDEX FOR (n:Gene) ON (n.description);
CREATE INDEX FOR (n:Gene) ON (n.idg2);
CREATE INDEX FOR (n:Gene) ON (n.tdl);
CREATE INDEX FOR (n:Gene) ON (n.fam);
CREATE INDEX FOR (n:Gene) ON (n.uniprot);
CREATE INDEX FOR (n:Signature) ON (n.cell_id);
CREATE INDEX FOR (n:Signature) ON (n.pert_id);
CREATE INDEX FOR (n:Signature) ON (n.pert_type);
CREATE INDEX FOR (n:Signature) ON (n.pert_idose);
CREATE INDEX FOR (n:Signature) ON (n.pert_iname);
