MATCH paths = (d:Concept {name:'Parkinson\'s disease'})-[*1..3]-(g:Gene)
WITH d,g,paths LIMIT 5
UNWIND paths AS pathz
UNWIND pathz AS path
WITH d,g,(NODES(path)) AS pnodes, REDUCE(tot=0.0, mnode IN NODES(path) | tot + SIZE((mnode)-[]-()) ^-.4) AS dwp
RETURN d.id,g.name, SIZE(pnodes) AS numberOfNodes, SUM(dwp) AS DWPC
ORDER BY DWPC DESC ;
