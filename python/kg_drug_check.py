#!/usr/bin/env python3
"""
Check which drugs are in KG.
"""
import sys,os,json,re,logging
import pandas as pd
import numpy as np
import neo4j

logging.basicConfig(level=logging.INFO)

###

dcdrugs = pd.read_csv("dcdrugs.tsv", "\t")
dcdrugs["pubchem_cid"] = dcdrugs["pubchem_cid"].astype(str)
logging.debug("DCDRUGS rows,cols: {},{}".format(dcdrugs.shape[0], dcdrugs.shape[1]))
logging.info("DCDRUGS columns: {}".format(str(list(dcdrugs.columns))))
logging.info("DCDRUGS PUBCHEM_CIDs: {}".format(dcdrugs['pubchem_cid'].nunique()))

###
# Connect to Neo4j db:
NeoUser = ""; NeoPass = "";
with open(os.environ["HOME"]+"/.neo4j.sh") as fin:
    while True:
        line = fin.readline()
        if not line: break
        if re.match('.*NEO4J_USERNAME=', line):
            NeoUser = re.sub(r'^.*NEO4J_USERNAME="?([^"]*)"?$', r'\1', line.rstrip())
        elif re.match('.*NEO4J_PASSWORD=', line):
            NeoPass = re.sub(r'^.*NEO4J_PASSWORD="?([^"]*)"?$', r'\1', line.rstrip())
    print("NeoUser: \"{}\"; NeoPass: \"{}\"\n".format(NeoUser, NeoPass))

uri = "neo4j://hoffmann.data2discovery.net:7695"
db = neo4j.GraphDatabase.driver(uri, auth= (NeoUser, NeoPass))
session = db.session()

cid_list = list(dcdrugs.pubchem_cid.array.astype('int'))

cql = """\
MATCH (d:Drug)
WHERE (d.pubchem_cid in {})
RETURN d
ORDER BY d.name
""".format(cid_list)
rdata = session.run(cql).data()
drugs = [val['d'] for val in rdata]
df = pd.DataFrame(drugs)
logging.info("columns: {}".format(str(list(df.columns))))

df["pubchem_cid"] = df["pubchem_cid"].astype(str)

logging.info("Drug PUBCHEM_CIDs in KG: {}/{} ({}%)".format(
	df['pubchem_cid'].nunique(),
	dcdrugs['pubchem_cid'].nunique(),
	100 * df['pubchem_cid'].nunique() / dcdrugs['pubchem_cid'].nunique()))

logging.info("Drug PUBCHEM_CIDs in KG: {}".format(",".join(list(df.pubchem_cid))))

logging.info("Drug PUBCHEM_CIDs missing from KG: {}".format(
	",".join(list(set(dcdrugs.pubchem_cid) - set(df.pubchem_cid)))))
logging.info("Drug NAMEs missing from KG: {}".format(
	",".join(list(set(dcdrugs.name) - set(df.name)))))

print(dcdrugs.loc[([cid not in list(df['pubchem_cid']) for cid in dcdrugs['pubchem_cid']]), ['name', 'pubchem_cid']])
