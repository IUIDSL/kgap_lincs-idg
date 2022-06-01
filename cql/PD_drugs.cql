MATCH (c:Concept)-[r:INDICATION]-(d:Drug) WHERE c.name =~ ".*Parkinson.*" RETURN c,d ;
