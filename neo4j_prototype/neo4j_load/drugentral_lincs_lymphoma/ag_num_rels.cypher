CALL apoc.periodic.iterate(
"MATCH (n)-[r]-() return n, count(r) as num_rels",
"set n.num_rels = num_rels",
{batchSize:1000, iterateList:true, parallel:true});

CALL apoc.periodic.iterate(
"MATCH (n) where not (n)--() return n",
"set n.num_rels = 0",
{batchSize:1000, iterateList:true, parallel:true});



