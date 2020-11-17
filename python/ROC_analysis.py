#!/usr/bin/env python3
"""
See also notebook.
"""
import sys,os,re,logging
import pandas as pd, pandas.io.sql
import psycopg2,psycopg2.extras
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import matthews_corrcoef, f1_score
from matplotlib import pyplot as plt
import neo4j
from statsmodels.distributions.empirical_distribution import ECDF

logging.basicConfig(level=logging.INFO)

###
def cypher2df(cql):
    "Run Cypher query, return dataframe."
    df = pd.DataFrame(session.run(cql).data())
    return(df)

###
def ROCplotter(results, valgenes, gene_tag_v = "name", gene_tag_r = "name", score_tag = "score",
	show_precision=True, show_recall=True, show_accuracy=False, show_mcc=False):
    """From query results and a validation geneset, plot ROC curve with AUC."""
    vga = np.array(results[gene_tag_r].isin(valgenes[gene_tag_v]).astype(np.int8))
    fpr, tpr, thresholds = roc_curve(vga, np.array(results[score_tag]))
    logging.info("ROC points (fpr, tpr, thresholds): ({}, {}, {})".format(len(fpr), len(tpr), len(thresholds)))
    logging.info("ROC thresholds: range: [{:.2f}, {:.2f}], mean:{:.2f}; median:{:.2f}".format(min(thresholds), max(thresholds), np.mean(thresholds), np.median(thresholds)))
    aucval = roc_auc_score(vga, np.array(results[score_tag]))
    plt.figure(figsize=(7,5), dpi=100)
    plt.plot(fpr, tpr, color='darkorange', lw=2, linestyle="-", label = 'ROC curve')
    plt.annotate("AUC: {:0.2f}\nresults: {}\npositives: {}".format(aucval, results.shape[0], len(tpr)), xy=(.8, .4), xycoords="axes fraction")
    plt.plot([0,1], [0,1], color ='lightgray', lw=1, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate (recall)')
    if show_precision:
      prec = [precision_score(vga, results[score_tag]>=t, zero_division=0) for t in thresholds]
      plt.plot(fpr, prec, color='cyan', lw=1, linestyle="-.", label='Precision (max={:.3f})'.format(max(prec)))
    if show_recall:
      recl = [recall_score(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, recl, color='green', lw=1, linestyle=":", label='Recall')
    if show_accuracy:
      acc = [accuracy_score(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, acc, color='gray', lw=1, label='Accuracy')
    if show_mcc:
      mccs = [matthews_corrcoef(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, mccs, color='darkgray', lw=1, label='MCC (max={:.3f})'.format(max(mccs)))
    plt.legend(loc="lower right")
    return(plt)

###
# Connect to DrugCentral:
dbhost="unmtid-dbs.net"; dbport=5433; dbname="drugcentral"; dbusr="drugman"; dbpw="dosage";
dsn = ("host='%s' port='%s' dbname='%s' user='%s' password='%s'"%(dbhost, dbport, dbname, dbusr, dbpw))
dbcon = psycopg2.connect(dsn)
dbcon.cursor_factory = psycopg2.extras.DictCursor

###
# Query DrugCentral for PD drugs:
sql = """\
SELECT DISTINCT
	ids.identifier AS pubchem_cid,
	s.id,
	s.name,
	s.smiles,
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
    AND omop.concept_name ~* 'Parkinson'
"""

dcdrugs = pandas.io.sql.read_sql_query(sql, dbcon)
logging.debug("rows,cols: {},{}".format(dcdrugs.shape[0], dcdrugs.shape[1]))
logging.info("Drug PUBCHEM_CIDs (N={}): {}".format(dcdrugs['pubchem_cid'].nunique(), ",".join(list(dcdrugs.pubchem_cid))))
dcdrugs.to_csv("../data/dcdrugs.tsv", "\t", index=False)

###
# Query DrugCentral for PD genes:
sql="""\
SELECT DISTINCT
        atf.target_name,
        atf.gene genes,
        atf.moa
FROM
        act_table_full atf
JOIN
        structures s ON s.id = atf.struct_id
JOIN
        omop_relationship omop ON omop.struct_id = s.id
JOIN
        struct2atc s2atc ON s2atc.struct_id = s.id
JOIN
       atc ON atc.code = s2atc.atc_code
WHERE
        omop.relationship_name = 'indication'
        AND omop.concept_name ~* 'Parkinson'
	AND atc.l1_name = 'NERVOUS SYSTEM'
"""
dcgenes = pandas.io.sql.read_sql_query(sql, dbcon)
dcgenes = dcgenes.astype({'moa': 'boolean'})
#print(dcgenes.head())
logging.info("Targets (pre-multi-split): {}".format(dcgenes['genes'].nunique()))
logging.info("Targets, MoA (pre-multi-split): {}".format(dcgenes[(dcgenes.moa)]['genes'].nunique()))
logging.info("Targets, MoA (pre-multi-split): {}".format(dcgenes[(dcgenes.moa)]['genes'].str.cat(sep=',')))

# Parse and split delimited gene symbols to separate rows:
b = pd.DataFrame(dcgenes.genes.str.split('|').tolist(), index=dcgenes.index).stack()
b = pd.DataFrame(b)
b.columns = ['gene']
logging.debug("0-level index: {}".format(b.index.levels[0]))
b = b.reset_index(level=1, drop=True)
dcgenes = dcgenes.drop(columns=["genes"]).join(b, how="left")
logging.info("Targets (post-multi-split): {}".format(dcgenes['gene'].nunique()))
logging.info("Targets, MoA (post-multi-split): {}".format(dcgenes[(dcgenes.moa)]['gene'].nunique()))
dcgenes.to_csv("../data/dcgenes.tsv", "\t", index=False)
#print(dcgenes.head(12))

###
# Connect to Neo4j db:
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
db = neo4j.GraphDatabase.driver(uri, auth= (NeoUser, NeoPass))
session = db.session()

cid_list = list(dcdrugs.pubchem_cid.array.astype('int'))

#score_attribute = "COUNT(distinct s)"

score_attribute = "sum(s.degree)"
cql_d = """\
MATCH p=(d:Drug)-[]-(s:Signature)-[r]-(g:Gene), p1=(s)-[]-(c:Cell)
WHERE (d.pubchem_cid in {})
WITH g, {} AS score
RETURN g.id, g.name, score
ORDER BY score DESC
""".format(cid_list, score_attribute)

logging.debug("CQL: {}".format(cql_d))
cdf_d = cypher2df(cql_d)
cdf_d.head(10)
# Save results
cdf_d.columns = ["ncbiGeneId", "geneSymbol", "kgapScore"]
#cdf_d.to_csv("../data/results_dweighted.tsv", "\t", index=False)

score_attribute = "sum(r.zscore)/sqrt(count(r))"  # sumz()
cql_z = """\
MATCH p=(d:Drug)-[]-(s:Signature)-[r]-(g:Gene), p1=(s)-[]-(c:Cell)
WHERE (d.pubchem_cid in {})
WITH g, {} AS score
RETURN g.id, g.name, score
ORDER BY score DESC
""".format(cid_list, score_attribute)

logging.debug("CQL: {}".format(cql_z))
cdf_z = cypher2df(cql_z)
cdf_z.head(10)
# Save results
cdf_z.columns = ["ncbiGeneId", "geneSymbol", "kgapScore"]
cdf_z.to_csv("../data/results_zweighted.tsv", "\t", index=False)

"""
 does not work, is there an index that must be altered?
 cdf.sort_values("g.name", axis=0, ascending=True)
"""

ecdf = ECDF(cdf_z.kgapScore)
plt.plot(ecdf.x, ecdf.y)
plt.title("KGAP-LINCS Z-weighted Score ECDF")
plt.savefig("../data/KGAP-LINCS_ScoreEcdf.png", format="png")

plt = ROCplotter(cdf_d, dcgenes, gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes, D-weighted')
plt.savefig("../data/KGAP-LINCS_ROC_Dweighted.png", format="png")

plt = ROCplotter(cdf_d, dcgenes[(dcgenes.moa)], gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes (MoA), D-weighted')
plt.savefig("../data/KGAP-LINCS_ROC_DweightedMoA.png", format="png")

plt = ROCplotter(cdf_z, dcgenes, gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes, Z-weighted')
plt.savefig("../data/KGAP-LINCS_ROC_Zweighted.png", format="png")

plt = ROCplotter(cdf_z, dcgenes[(dcgenes.moa)], gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes (MoA), Z-weighted')
plt.savefig("../data/KGAP-LINCS_ROC_ZweightedMoA.png", format="png")
#plt.show()

