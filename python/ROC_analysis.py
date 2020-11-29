#!/usr/bin/env python3
"""
See also notebook.
"""
import sys,os,re,logging,argparse
import pandas as pd, pandas.io.sql
import psycopg2,psycopg2.extras
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import matthews_corrcoef, f1_score
from matplotlib import pyplot as plt
import neo4j
from statsmodels.distributions.empirical_distribution import ECDF

###
def cypher2df(cql):
    "Run Cypher query, return dataframe."
    df = pd.DataFrame(session.run(cql).data())
    return(df)

###
def ROCplotter(results, valgenes, gene_tag_v = "name", gene_tag_r = "name", score_tag = "score",
	show_precision=True, show_recall=True, show_accuracy=False, show_mcc=False, title="ROC Plot"):
    """From query results and a validation geneset, plot ROC curve with AUC."""
    vga = np.array(results[gene_tag_r].isin(valgenes[gene_tag_v]).astype(np.int8))
    fpr, tpr, thresholds = roc_curve(vga, np.array(results[score_tag]))
    logging.info("ROC points (fpr, tpr, thresholds): ({}, {}, {})".format(len(fpr), len(tpr), len(thresholds)))
    logging.info("ROC thresholds: range: [{:.2f}, {:.2f}], mean:{:.2f}; median:{:.2f}".format(min(thresholds), max(thresholds), np.mean(thresholds), np.median(thresholds)))
    aucval = roc_auc_score(vga, np.array(results[score_tag]))
    logging.info("AUC: {:0.2f}; results: {}; positives: {}".format(aucval, results.shape[0], len(tpr)))
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
    plt.title(title)
    return(plt)

###
def DrugCentralConnect(dbhost ,dbport, dbname, dbusr, dbpw):
  """Connect to DrugCentral."""
  dsn = (f"host='{dbhost}' port='{dbport}' dbname='{dbname}' user='{dbusr}' password='{dbpw}'")
  dbcon = psycopg2.connect(dsn)
  dbcon.cursor_factory = psycopg2.extras.DictCursor
  return dbcon

###
def GetIndication2Drugs(indication_query, atc_query):
  """Query DrugCentral from indication for drugs."""
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
LEFT JOIN
        struct2atc s2atc ON s2atc.struct_id = s.id
LEFT JOIN
       atc ON atc.code = s2atc.atc_code
WHERE
	ids.id_type = 'PUBCHEM_CID'
	AND omop.relationship_name = 'indication'
	AND omop.concept_name ~* '{}'
""".format(indication_query)
  if atc_query: sql += """ AND atc.l1_name ~* '{}'""".format(atc_query)
  logging.info(sql)
  dcdrugs = pandas.io.sql.read_sql_query(sql, dbcon)
  logging.debug("rows,cols: {},{}".format(dcdrugs.shape[0], dcdrugs.shape[1]))
  return dcdrugs

###
def GetIndication2Genes(indication_query, atc_query):
  """Query DrugCentral from indication for genes."""
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
LEFT JOIN
	struct2atc s2atc ON s2atc.struct_id = s.id
LEFT JOIN
	atc ON atc.code = s2atc.atc_code
WHERE
	atf.gene IS NOT NULL
	AND omop.relationship_name = 'indication'
	AND omop.concept_name ~* '{}'
""".format(indication_query)
  if atc_query: sql += """ AND atc.l1_name ~* '{}'""".format(atc_query)
  logging.info(sql)
  dcgenes = pandas.io.sql.read_sql_query(sql, dbcon)
  dcgenes = dcgenes.astype({'moa': 'boolean'})
  logging.debug("Targets (pre-multi-split): {}".format(dcgenes['genes'].nunique()))
  logging.debug("Targets, MoA (pre-multi-split) ({}): {}".format(dcgenes[(dcgenes.moa)]['genes'].nunique(), dcgenes[(dcgenes.moa)]['genes'].str.cat(sep=',')))

  if dcgenes.shape[0]>0:
    # Parse and split delimited gene symbols to separate rows:
    b = pd.DataFrame(dcgenes.genes.str.split('|').tolist(), index=dcgenes.index).stack()
    b = pd.DataFrame(b)
    b.columns = ['gene']
    logging.debug("0-level index: {}".format(b.index.levels[0]))
    b = b.reset_index(level=1, drop=True)
    dcgenes = dcgenes.drop(columns=["genes"]).join(b, how="left")
  return dcgenes

###
def Neo4jConnect(uri, paramfile):
  """Connect to Neo4j db."""
  NeoUser=""; NeoPass="";
  with open(paramfile) as fin:
    while True:
      line = fin.readline()
      if not line: break
      if re.match('.*NEO4J_USERNAME=', line):
        NeoUser = re.sub(r'^.*NEO4J_USERNAME="?([^"]*)"?$', r'\1', line.rstrip())
      elif re.match('.*NEO4J_PASSWORD=', line):
        NeoPass = re.sub(r'^.*NEO4J_PASSWORD="?([^"]*)"?$', r'\1', line.rstrip())
    logging.debug("NeoUser: \"{}\"; NeoPass: \"{}\"".format(NeoUser, NeoPass))

  neo4jdb = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NeoUser, NeoPass))
  session = neo4jdb.session()
  return session

###
def KGAP_Search(cid_list, score_attribute):
  cql = """\
MATCH p=(d:Drug)-[]-(s:Signature)-[r]-(g:Gene), p1=(s)-[]-(c:Cell)
WHERE (d.pubchem_cid in {})
WITH g, {} AS score
RETURN g.id, g.name, score
ORDER BY score DESC
""".format(cid_list, score_attribute)
  logging.debug("CQL: {}".format(cql))
  cdf = cypher2df(cql)
  cdf.columns = ["ncbiGeneId", "geneSymbol", "kgapScore"]
  return cdf

###
if __name__=="__main__":
  DC_DBHOST="unmtid-dbs.net"; DC_DBPORT=5433; DC_DBNAME="drugcentral";
  DC_DBUSR="drugman"; DC_DBPW="dosage";
  NEO4J_URI = "neo4j://hoffmann.data2discovery.net:7695"
  NEO4J_PARAMFILE = os.environ["HOME"]+"/.neo4j.sh"
  #INDICATION_QUERY = "Parkinson"; ATC_QUERY = 'NERVOUS SYSTEM';
  parser = argparse.ArgumentParser(description='KGAP LINCS-IDG ROC analysis')
  parser.add_argument("--indication_query", required=True, help="DrugCentral indication query")
  parser.add_argument("--atc_query", help="DrugCentral ATC L1 query")
  parser.add_argument("--odir", default=".", help="output dir")
  parser.add_argument("--dc_dbhost", default=DC_DBHOST, help="DrugCentral DBHOST")
  parser.add_argument("--dc_dbport", type=int, default=DC_DBPORT, help="DrugCentral DBPORT")
  parser.add_argument("--dc_dbname", default=DC_DBNAME, help="DrugCentral DBNAME")
  parser.add_argument("--dc_dbusr", default=DC_DBUSR, help="DrugCentral DBUSR")
  parser.add_argument("--dc_dbpw", default=DC_DBPW, help="DrugCentral DBPW")
  parser.add_argument("--neo4j_uri", default=NEO4J_URI, help="Neo4j DB URI")
  parser.add_argument("--neo4j_paramfile", default=NEO4J_PARAMFILE, help="Neo4j parameter file")
  parser.add_argument("-v", "--verbose", dest="verbose", action="count", default=0)
  args = parser.parse_args()

  logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.DEBUG if args.verbose>1 else logging.INFO))

  dbcon = DrugCentralConnect(args.dc_dbhost, args.dc_dbport, args.dc_dbname, args.dc_dbusr, args.dc_dbpw)

  dcdrugs = GetIndication2Drugs(args.indication_query, args.atc_query)
  if dcdrugs.shape[0]==0:
    logging.info(f"No drugs found for {args.indication_query}.  Quitting.")
    sys.exit(0)
  logging.info("Drug PUBCHEM_CIDs (N={}): {}".format(dcdrugs['pubchem_cid'].nunique(), ",".join(list(dcdrugs.pubchem_cid.unique()))))
  dcdrugs.to_csv(f"{args.odir}/dcdrugs.tsv", "\t", index=False)

  dcgenes = GetIndication2Genes(args.indication_query, args.atc_query)
  if dcgenes.shape[0]==0:
    logging.info(f"No genes found for {args.indication_query}.  Quitting.")
    sys.exit(0)
  logging.info("Targets: {}".format(dcgenes['gene'].nunique()))
  logging.info("Targets, MoA: {}".format(dcgenes[(dcgenes.moa)]['gene'].nunique()))
  dcgenes.to_csv(f"{args.odir}/dcgenes.tsv", "\t", index=False)
  #print(dcgenes.head(12))

  ###
  session = Neo4jConnect(NEO4J_URI, args.neo4j_paramfile)

  cid_list = list(dcdrugs.pubchem_cid.array.astype('int'))

  ###
  # Degree-weighted:
  #score_attribute = "sum(s.degree)"
  #cdf_d = KGAP_Search(cid_list, score_attribute)
  #cdf_d.head(10)
  #cdf_d.to_csv(f"{args.odir}/results_dweighted.tsv", "\t", index=False)

  #plt = ROCplotter(cdf_d, dcgenes, gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes, D-weighted ({args.indication_query})')
  #plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_Dweighted.png", format="png")
  
  #plt = ROCplotter(cdf_d, dcgenes[(dcgenes.moa)], gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes (MoA), D-weighted ({args.indication_query})')
  #plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_DweightedMoA.png", format="png")

  ###
  # Z-score-(and-degree)-weighted:
  score_attribute = "sum(r.zscore)/sqrt(count(r))"  # sumz()
  cdf_z = KGAP_Search(cid_list, score_attribute)
  cdf_z.head(10)
  cdf_z.to_csv(f"{args.odir}/results_zweighted.tsv", "\t", index=False)

  ecdf_z = ECDF(cdf_z.kgapScore)
  plt.plot(ecdf_z.x, ecdf_z.y)
  plt.title("KGAP-LINCS Z-weighted Score ECDF")
  plt.savefig(f"{args.odir}/KGAP-LINCS_ScoreEcdf.png", format="png")

  plt = ROCplotter(cdf_z, dcgenes, gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes, Z-weighted\n({args.indication_query})')
  plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_Zweighted_{args.indication_query}.png", format="png")

  plt = ROCplotter(cdf_z, dcgenes[(dcgenes.moa)], gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes (MoA), Z-weighted\n({args.indication_query})')
  plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_ZweightedMoA_{args.indication_query}.png", format="png")
  #plt.show()

