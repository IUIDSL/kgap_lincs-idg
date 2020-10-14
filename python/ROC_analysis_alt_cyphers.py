"""
Based on Dan Bieber's notebook.
"""
import sys, os, re, logging
import pandas as pd
import pandas.io.sql
import psycopg2, psycopg2.extras
import requests
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot as plt
import neo4j

logging.basicConfig(level=logging.INFO)

###
def cypher2df(cql):
    """Run Cypher query, return dataframe."""
    df = pd.DataFrame(session.run(cql).data())
    return(df)

###
def ROCplotter(results, valgenes, gene_tag_v = "name", gene_tag_r = "name", score_tag = "score"):
    """From query results and a validation geneset, plot ROC curve with AUC."""

    "Bit vector - 1 if Gene is in valgenes['g.name'] AND in results['gene']"
    vga = np.array(results[gene_tag_r].isin(valgenes[gene_tag_v]).astype(np.int8))
    fpr, tpr, thresholds = roc_curve(vga, np.array(results[score_tag]))
    logging.info("ROC points (fpr, tpr, thresholds): ({}, {}, {})".format(len(fpr), len(tpr), len(thresholds)))
    aucval = roc_auc_score(vga, np.array(results[score_tag]))
    plt.figure(figsize=(7,5), dpi=100)
    plt.plot(fpr, tpr, color='darkorange', lw=1, label = 'ROC curve')
    plt.annotate("AUC: {:0.2f}\nresults: {}\npositives: {}\nfalse positives: {}".format(aucval, results.shape[0], len(tpr), len(fpr)), xy=(.7, .4), xycoords="axes fraction")
    plt.plot([0,1], [0,1], color ='blue', lw=1, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    return(plt)

###
url = "https://raw.githubusercontent.com/IUIDSL/kgap_lincs-idg/master/py_nb/DrugCentral_PD_targets.tsv"
dcgenes = pd.read_csv(url, sep="\t")
dcgenes.columns = ["target_name", "genes", "moa"]
dcgenes = dcgenes.astype({'moa': 'boolean'})
print(dcgenes.head())

b = pd.DataFrame(dcgenes.genes.str.split('|').tolist(), index=dcgenes.index).stack()
b = pd.DataFrame(b)
b.columns = ['gene']
print("0-level index: {}".format(b.index.levels[0]))
b.head()
b = b.reset_index(level=1, drop=True)

dcgenes = dcgenes.drop(columns=["genes"]).join(b, how="left")
print(dcgenes.head(12))

with open(os.environ["HOME"]+"/.neo4j.sh") as fin:
    NeoUser = ""
    NeoPass = ""
    while True:
        line = fin.readline()
        if not line: break
        if re.match('.*NEO4J_USERNAME=', line):
            NeoUser = re.sub(r'^.*NEO4J_USERNAME="?([^"]*)"?$', r'\1', line.rstrip())
        elif re.match('.*NEO4J_PASSWORD=', line):
            NeoPass = re.sub(r'^.*NEO4J_PASSWORD="?([^"]*)"?$', r'\1', line.rstrip())
    print("NeoUser: \"{}\"; NeoPass: \"{}\"\n".format(NeoUser, NeoPass))

uri = "neo4j://hoffmann.data2discovery.net:7695"
#uri = "neo4j://localhost:7695"
db = neo4j.GraphDatabase.driver(uri, auth= (NeoUser, NeoPass))
session = db.session()


dbhost="unmtid-dbs.net"; dbport=5433; dbname="drugcentral"; dbusr="drugman"; dbpw="dosage";
dsn = ("host='%s' port='%s' dbname='%s' user='%s' password='%s'"%(dbhost, dbport, dbname, dbusr, dbpw))
dbcon = psycopg2.connect(dsn)
dbcon.cursor_factory = psycopg2.extras.DictCursor

sql = """\
SELECT DISTINCT
	ids.identifier AS pubchem_cid,
	s.id,
	s.name,
	atc.l1_code,
	atc.l1_name,
	omop.concept_name omop_concept_name,
	omop.snomed_full_name
FROM
	omop_relationship omop
JOIN
	structures s ON omop.struct_id = s.id
JOIN
	identifier ids ON ids.struct_id = s.id
JOIN
        struct2atc s2atc ON s2atc.struct_id = s.id
JOIN
       atc ON atc.code = s2atc.atc_code
WHERE
	ids.id_type = 'PUBCHEM_CID'
	AND atc.l1_name = 'NERVOUS SYSTEM'
	AND omop.relationship_name = 'indication'
"""
#	AND (
#	(omop.concept_name ~* 'Parkinson' OR omop.snomed_full_name ~* 'Parkinson')
#	OR (omop.concept_name ~* 'dyskinesia' OR omop.snomed_full_name ~* 'dyskinesia')
#	)

df = pandas.io.sql.read_sql_query(sql, dbcon)
logging.info("rows,cols: {},{}".format(df.shape[0], df.shape[1]))
logging.info("drug (pubchem_cid) count: {}".format(df['pubchem_cid'].nunique()))
for omop_concept_name in df['omop_concept_name'].sort_values().unique():
    logging.info("omop_concept_name: \"{}\"".format(omop_concept_name))
for snomed_full_name in df['snomed_full_name'].sort_values().unique():
    logging.info("snomed_full_name: \"{}\"".format(snomed_full_name))
#df.to_csv(sys.stdout, "\t")

logging.info("PUBCHEM_CIDs: {}".format(df.pubchem_cid.str.join(",")))

#cqlurl = "https://raw.githubusercontent.com/IUIDSL/kgap_lincs-idg/master/cql/pd-adamic-adar.cql"
#cql = requests.get(cqlurl).text
#, p1=(s)-[]-(c:Cell)"

score_attribute = "sum(s.degree)"
#score_attribute = "sum(r.zscore)"
#score_attribute = "COUNT(distinct s)"      # distinct s = s ?
#WHERE (toInteger(d.pubchem_cid) in [ {} ])

cid_list = list(df.pubchem_cid.array.astype('int'))

cql = """\
MATCH p=(d:Drug)-[]-(s:Signature)-[r]-(g:Gene), p1=(s)-[]-(c:Cell)
WHERE (d.pubchem_cid in {})
WITH g, {} AS score
RETURN g.id, g.name, score
ORDER BY score DESC
""".format(cid_list, score_attribute)

print("CQL: {}\n", cql)
cdf = cypher2df(cql)
cdf.head(10)

"""
 does not work, is there an index that must be altered?
 cdf.sort_values("g.name", axis=0, ascending=True)
"""
plt = ROCplotter(cdf, dcgenes[(dcgenes.moa)], gene_tag_r = "g.name", gene_tag_v="gene", score_tag = "score")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes (MoA)')
plt.show()
