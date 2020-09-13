"""
Based on Dan Bieber's notebook.
"""
import sys,os,re,logging
import pandas as pd
import requests
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot as plt
import neo4j

logging.basicConfig(level=logging.INFO)

###
def cypher2df(cql):
    "Run Cypher query, return dataframe."
    df = pd.DataFrame(session.run(cql).data())
    return(df)

###
def ROCplotter(results, valgenes, gene_tag_v = "name", gene_tag_r = "name", score_tag = "score"):
    """From query results and a validation geneset, plot ROC curve with AUC."""
    vga = np.array(results[gene_tag_r].isin(valgenes[gene_tag_v]).astype(np.int8))
    fpr, tpr, thresholds = roc_curve(vga, np.array(results[score_tag]))
    logging.info("ROC points (fpr, tpr, thresholds): ({}, {}, {})".format(len(fpr), len(tpr), len(thresholds)))
    aucval = roc_auc_score(vga, np.array(results[score_tag]))
    plt.figure(figsize=(7,5), dpi=100)
    plt.plot(fpr, tpr, color='darkorange', lw=1, label = 'ROC curve')
    plt.annotate("AUC: {:0.2f}\nresults: {}\npositives: {}".format(aucval, results.shape[0], len(tpr)), xy=(.8, .4), xycoords="axes fraction")
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
db = neo4j.GraphDatabase.driver(uri, auth= (NeoUser, NeoPass))
session = db.session()

cqlurl = "https://raw.githubusercontent.com/IUIDSL/kgap_lincs-idg/master/cql/pd-adamic-adar.cql"
cql = requests.get(cqlurl).text
print("CQL: {}\n".format(cql))
cdf = cypher2df(cql)
cdf.head(10)

plt = ROCplotter(cdf, dcgenes[(dcgenes.moa)], gene_tag_r = "gd.name", gene_tag_v="gene", score_tag = "score")
plt.title('KGAP-LINCS ROC vs DrugCentral PD Genes (MoA)')
plt.show()
