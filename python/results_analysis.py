#!/usr/bin/env python3
"""
Analyze hitlists from KGAP-LINCS, by joining with IDG.
"""

import sys,os,logging
import pandas as pd
import mysql.connector as mysql

from BioClients.idg import tcrd as bc_tcrd
from BioClients.util import yaml as bc_yaml
from BioClients import chembl as bc_chembl
from BioClients import pubchem as bc_pubchem

logging.basicConfig(level=logging.INFO)

results = pd.read_csv("results_zweighted.tsv", "\t")

logging.info("results: {}x{}; {}".format(results.shape[0], results.shape[1], (','.join(list(results.columns)))))

# Sort by score, keep top hits only.
results = results.sort_values(by=['kgapScore'], ascending=[False])
results = results.iloc[1:100,]
print(results.head(10))

params = bc_yaml.ReadParamFile(os.environ['HOME']+"/.tcrd.yaml")
dbcon = mysql.connect(host=params['DBHOST'], port=params['DBPORT'], user=params['DBUSR'], passwd=params['DBPW'], db=params['DBNAME'])

tcrd = bc_tcrd.GetTargets(dbcon, list(results.geneSymbol), "GENESYMBOL", fout=None)
print(tcrd.head(10))

results = pd.merge(results, tcrd, left_on="geneSymbol", right_on="protein_sym")
logging.info("results: {}x{}; {}".format(results.shape[0], results.shape[1], (','.join(list(results.columns)))))
for tag in ["target_tdl", "target_fam"]:
  for key, val in results[tag].value_counts().iteritems():
    logging.info('\t{}: {:6d}: {}'.format(tag, val, key))
results.to_csv("results_tcrd.tsv", sep="\t")