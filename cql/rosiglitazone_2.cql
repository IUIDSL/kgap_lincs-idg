// Projection of the Gene Signature Drug onto Gene-Drug graph
// Ie signature effectively as an edge (removed as a node)
// Red -upregulared, green down +- 8 zscore
// 
// This view shows the common genes between troglitazone and
// rosiglitazone Along with degree of commonality expressed as size of
// the gene node Towards representing signature patterns in a network
// form Interesting those genes which zscore inversions between the 2
// similar drugs These 2 drugs chosen based on the link prediction work
// already published by David Wild.

match p=(rg:Drug {id:'2405'})-[:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(g), p2=(s)-[:CELL_SIGNATURE]-()  
//where sg.zscore > 8 or sg.zscore < -8
return rg.id as sn, sg.zscore as ed, g.pr_gene_symbol as en, "gene" as type, count(p) as x
union
match p=(rg:Drug {id:'2405'})-[:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(), p2=(s)-[cs:CELL_SIGNATURE]-(cell)  
//where sg.zscore >8 or sg.zscore < -8
return rg.id as sn, cs as ed, cell.id as en, "cell" as type, count(p) as x
union
match p=(rg:Drug {id:'2767'})-[:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(g), p2=(s)-[:CELL_SIGNATURE]-()  
//where sg.zscore > 8 or sg.zscore < -8
return rg.id as sn, sg.zscore as ed, g.pr_gene_symbol as en, "gene" as type, count(p) as x
union
match p=(rg:Drug {id:'2767'})-[:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(), p2=(s)-[cs:CELL_SIGNATURE]-(cell)  
//where sg.zscore > 8 or sg.zscore < -8
return rg.id as sn, cs as ed, cell.id as en, "cell" as type,count(p) as x
;
