// Tdark - max signatures in graph
// Top 5 tdark genes by signature count in the graph

match (g:Gene)-[sg:SIGNATURE_GENE]-() where g.tdl="Tdark"
with g, count(sg) as sgc 
order by sgc desc
limit 5
match p=(g)-[r:SIGNATURE_GENE]-(s)-[:DRUG_SIGNATURE]-(d),p2=(s)-[:CELL_SIGNATURE]-(c) where r.zscore >8 or r.zscore <-8
return g.pr_gene_symbol as sn, c.id+"^"+s.id as rel, r.zscore, c.cell_lineage, d.id as en, d.pert_iname as enm, "drug" as entype limit 100
;
