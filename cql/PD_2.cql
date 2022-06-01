MATCH p=((c:Concept)
        -[r:INDICATION]-(d:Drug)
        -[ds:DRUG_SIGNATURE]-(s:Signature)
        -[sg:SIGNATURE_GENE]-(g:Gene))
WHERE c.name =~ ".*Parkinson.*disease.*"
RETURN DISTINCT d.name, d.pubchem_cid, d.pert_id, d.canonical_smiles
LIMIT 200
	;
