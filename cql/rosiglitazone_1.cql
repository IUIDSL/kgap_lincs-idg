// Network overview showing rosiglitazone drug with signatures in circle,
// genes in the middle, cell tissue outside circle Edges Red-upregulated
// Signature nodes - gray Genes closer together are more topologically
// similar which in this case means they share co-occurrence profiles in
// signatures up/down regulation filtered at +-6 (in cytoscape)

match p=(rg:Drug {id:'2405'})-[:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(), p2=(s)-[:CELL_SIGNATURE]-()
where sg.zscore > 6 or sg.zscore < -6
with relationships(p)+relationships(p2) as relz
unwind relz as rel
return startNode(rel),rel,endNode(rel)
union
match p=(rg:Drug {id:'2767'})-[ds:DRUG_SIGNATURE]-(s)-[sg:SIGNATURE_GENE]-(), p2=(s)-[:CELL_SIGNATURE]-()
where sg.zscore > 6 or sg.zscore < -6
with relationships(p)+relationships(p2) as relz
unwind relz as rel
return startNode(rel),rel,endNode(rel)
;
