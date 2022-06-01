MATCH p=((c:Concept)
        -[r:INDICATION]-(d:Drug)
        -[ds:DRUG_SIGNATURE]-(s:Signature)
        -[sg:SIGNATURE_GENE]-(g:Gene))
WHERE c.name =~ ".*Parkinson.*disease.*"
RETURN p
LIMIT 30
	;
