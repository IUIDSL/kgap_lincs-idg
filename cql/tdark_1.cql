//TDARK-
//Tdark gene with lowest number of signatures filtered at +-8 zscore
//signature-gray

match (g:Gene {id:'94239'}) where g.tdl ="Tdark" 
with g
match p=(g)-[r:SIGNATURE_GENE]-(s)-[:DRUG_SIGNATURE]-(),p2=(s)-[:CELL_SIGNATURE]-() where r.zscore >8 or r.zscore <-8
with relationships(p) +relationships(p2) as relz
unwind relz as rel
return startNode(rel),rel,endNode(rel) 
;
