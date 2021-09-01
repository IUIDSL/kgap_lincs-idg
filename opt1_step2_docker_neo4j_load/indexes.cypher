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

// commonly searched properties?
CREATE INDEX FOR (n:Gene) ON (n.pr_gene_title);
CREATE INDEX FOR (n:Gene) ON (n.description);
