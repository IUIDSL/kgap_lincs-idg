// Restricted drug set based on less-comorbid/confounded indications.
MATCH p=(d:Drug)-[]-(s:Signature)-[]-(g:Gene), p1=(s)-[]-(c:Cell) 
WHERE
	c.cell_lineage = "central nervous system"
AND (	d.pubchem_cid='2130'
	OR d.pubchem_cid='6005'
	OR d.pubchem_cid='1201549'
	OR d.pubchem_cid='2381'
	OR d.pubchem_cid='31101'
	OR d.pubchem_cid='34359'
	OR d.pubchem_cid='2911'
	OR d.pubchem_cid='30843'
	OR d.pubchem_cid='92974'
	OR d.pubchem_cid='5281081'
	OR d.pubchem_cid='6047'
	OR d.pubchem_cid='23497'
	OR d.pubchem_cid='4167'
	OR d.pubchem_cid='4601'
	OR d.pubchem_cid='47811'
	OR d.pubchem_cid='4850'
	OR d.pubchem_cid='119570'
	OR d.pubchem_cid='4919'
	OR d.pubchem_cid='77991'
	OR d.pubchem_cid='5095'
	OR d.pubchem_cid='59227'
	OR d.pubchem_cid='26757'
	OR d.pubchem_cid='5374'
	OR d.pubchem_cid='4659569'
	OR d.pubchem_cid='5572'
	OR d.pubchem_cid='3052776'
	OR d.pubchem_cid='5311037'
	OR d.pubchem_cid='131682'
	OR d.pubchem_cid='10071196'
	OR d.pubchem_cid='76966913')
WITH g, count(DISTINCT s) AS sc
RETURN g.id, g.name, sc
ORDER BY sc DESC
