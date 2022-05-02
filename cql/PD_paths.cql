MATCH
	(c:Concept {name:'Parkinson\'s disease'})<-[ind:INDICATION]-(d:Drug)
	-[ds:DRUG_SIGNATURE]->(s:Signature)-[sg:SIGNATURE_GENE]->(g:Gene)
	RETURN c,d,s,g
	;
