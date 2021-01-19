#!/usr/bin/env python3
"""
Client for KGAP_LINCS-IDG drug target illumination method, as applied to 
Parkinson's disease.
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
	show_precision=False, show_recall=False, show_accuracy=False, show_mcc=False, title="ROC Plot"):
    """From query results and a validation geneset, plot ROC curve with AUC."""
    vga = np.array(results[gene_tag_r].isin(valgenes[gene_tag_v]).astype(np.int8))
    fpr, tpr, thresholds = roc_curve(vga, np.array(results[score_tag]))
    logging.info(f"ROC points (fpr, tpr, thresholds): ({len(fpr)}, {len(tpr)}, {len(thresholds)})")
    logging.info(f"ROC thresholds: range: [{min(thresholds):.2f}, {max(thresholds):.2f}], mean:{np.mean(thresholds):.2f}; median:{np.median(thresholds):.2f}")
    aucval = roc_auc_score(vga, np.array(results[score_tag]))
    logging.info(f"AUC: {aucval:0.2f}; results: {results.shape[0]}; positives: {len(tpr)}")
    plt.figure(figsize=(7,5), dpi=100)
    plt.plot(fpr, tpr, color='darkorange', lw=2, linestyle="-", label='ROC curve')
    plt.annotate(f"AUC: {aucval:0.2f}\nresults: {results.shape[0]}\npositives: {len(tpr)}", xy=(.8, .4), xycoords="axes fraction")
    plt.plot([0,1], [0,1], color ='lightgray', lw=1, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate (recall)')
    if show_precision:
      prec = [precision_score(vga, results[score_tag]>=t, zero_division=0) for t in thresholds]
      plt.plot(fpr, prec, color='cyan', lw=1, linestyle="-.", label=f"Precision (max={max(prec):.3f})")
    if show_recall:
      recl = [recall_score(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, recl, color='green', lw=1, linestyle=":", label='Recall')
    if show_accuracy:
      acc = [accuracy_score(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, acc, color='gray', lw=1, label='Accuracy')
    if show_mcc:
      mccs = [matthews_corrcoef(vga, results[score_tag]>=t) for t in thresholds]
      plt.plot(fpr, mccs, color='darkgray', lw=1, label=f"MCC (max={max(mccs):.3f})")
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
def GetIndication2Drugs(indication_query, indication_query_type, atc_query, atc_query_type):
  """Query DrugCentral from indication for drugs."""
  sql = f"""\
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
"""
  if indication_query_type=="exact":
    sql += f"        AND omop.concept_name ILIKE '{indication_query}'"
  elif indication_query_type=="substring":
    sql += f"        AND omop.concept_name ILIKE '%{indication_query}%'"
  else: #regex
    sql += f"        AND omop.concept_name ~* '{indication_query}'"
  if atc_query:
    if atc_query_type=="exact":
      sql += f" AND atc.l1_name ILIKE '{atc_query}'"
    elif atc_query_type=="substring":
      sql += f" AND atc.l1_name ILIKE '%{atc_query}%'"
    else: #regex
      sql += f" AND atc.l1_name ~* '{atc_query}'"
  logging.info(sql)
  dcdrugs = pandas.io.sql.read_sql_query(sql, dbcon)
  logging.debug(f"rows,cols: {dcdrugs.shape[0]},{dcdrugs.shape[1]}")
  return dcdrugs

###
def GetIndication2Genes(indication_query, indication_query_type, atc_query, atc_query_type):
  """Query DrugCentral from indication for genes."""
  sql = f"""\
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
"""
  if indication_query_type=="exact":
    sql += f"        AND omop.concept_name ILIKE '{indication_query}'"
  elif indication_query_type=="substring":
    sql += f"        AND omop.concept_name ILIKE '%{indication_query}'%"
  else: #regex
    sql += f"        AND omop.concept_name ~* '{indication_query}'"
  if atc_query:
    if atc_query_type=="exact":
      sql += f" AND atc.l1_name ILIKE '{atc_query}'"
    elif atc_query_type=="substring":
      sql += f" AND atc.l1_name ILIKE '%{atc_query}%'"
    else: #regex
      sql += f" AND atc.l1_name ~* '{atc_query}'"
  logging.info(sql)
  dcgenes = pandas.io.sql.read_sql_query(sql, dbcon)
  dcgenes = dcgenes.astype({'moa': 'boolean'})
  logging.debug(f"Targets (pre-multi-split): {dcgenes['genes'].nunique()}")
  logging.debug(f"Targets, MoA (pre-multi-split) ({dcgenes[(dcgenes.moa)]['genes'].nunique()}): {dcgenes[(dcgenes.moa)]['genes'].str.cat(sep=',')}")

  if dcgenes.shape[0]>0:
    # Parse and split delimited gene symbols to separate rows:
    b = pd.DataFrame(dcgenes.genes.str.split('|').tolist(), index=dcgenes.index).stack()
    b = pd.DataFrame(b)
    b.columns = ['gene']
    logging.debug(f"0-level index: {b.index.levels[0]}")
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
      if re.match('[^#]*NEO4J_USERNAME=', line):
        NeoUser = re.sub(r'^[^#]*NEO4J_USERNAME="?([^"]*)"?$', r'\1', line.rstrip())
      elif re.match('[^#]*NEO4J_PASSWORD=', line):
        NeoPass = re.sub(r'^[^#]*NEO4J_PASSWORD="?([^"]*)"?$', r'\1', line.rstrip())
    logging.debug(f"NeoUser: \"{NeoUser}\"; NeoPass: \"{NeoPass}\"")
  neo4jdb = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NeoUser, NeoPass))
  session = neo4jdb.session()
  return session

###
def KGAP_Search(cid_list, score_attribute):
  cql = f"""\
MATCH p=(d:Drug)-[]-(s:Signature)-[r]-(g:Gene), p1=(s)-[]-(c:Cell)
WHERE (d.pubchem_cid in {cid_list})
WITH g, {score_attribute} AS score
RETURN g.id, g.name, score
ORDER BY score DESC
"""
  logging.info(f"CQL: {cql}")
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
  ALGORITHMS=["dweighted", "zweighted"]
  QUERY_TYPES=["exact", "substring", "regex"]
  parser = argparse.ArgumentParser(description='KGAP LINCS-IDG search and ROC analysis')
  parser.add_argument("--indication_query", required=True, help="DrugCentral indication query")
  parser.add_argument("--indication_query_type", choices=QUERY_TYPES, default="regex")
  parser.add_argument("--atc_query", help="DrugCentral ATC L1 query")
  parser.add_argument("--atc_query_type", choices=QUERY_TYPES, default="regex")
  parser.add_argument("--odir", default=".", help="output dir")
  parser.add_argument("--algorithm", choices=ALGORITHMS, default="zweighted", help="graph analytic path scoring algorithm")
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

  dcdrugs = GetIndication2Drugs(args.indication_query, args.indication_query_type, args.atc_query, args.atc_query_type)
  if dcdrugs.shape[0]==0:
    logging.info(f"No drugs found for {args.indication_query}.  Quitting.")
    sys.exit(0)
  cid_list = sorted(list(dcdrugs.pubchem_cid.unique().astype('int')))
  logging.info(f"Drug PUBCHEM_CIDs (N={dcdrugs['pubchem_cid'].nunique()}): {str(cid_list)}")
  dcdrugs.to_csv(f"{args.odir}/dcdrugs_{args.indication_query}.tsv", "\t", index=False)

  dcgenes = GetIndication2Genes(args.indication_query, args.indication_query_type, args.atc_query, args.atc_query_type)
  if dcgenes.shape[0]==0:
    logging.info(f"No genes found for {args.indication_query}.  Quitting.")
    sys.exit(0)
  logging.info(f"Targets: {dcgenes['gene'].nunique()}")
  logging.info(f"Targets, MoA: {dcgenes[(dcgenes.moa)]['gene'].nunique()}")
  dcgenes.to_csv(f"{args.odir}/dcgenes_{args.indication_query}.tsv", "\t", index=False)

  ###
  session = Neo4jConnect(NEO4J_URI, args.neo4j_paramfile)

  ###
  if args.algorithm=="dweighted": # D-weighted: Degree-weighted
    score_attribute = "sum(s.degree)"
  elif args.algorithm=="zweighted": # Z-weighted: Z-score-and-degree-weighted, Stouffer's method
    score_attribute = "sum(r.zscore)/sqrt(count(r))"  
  else:
    parser.error(f"Invalid algorithm: {args.algorithm}")
    parser.print_help()

  ###
  cdf = KGAP_Search(cid_list, score_attribute)
  cdf.to_csv(f"{args.odir}/results_{args.indication_query}_{args.algorithm}.tsv", "\t", index=False)

  ecdf = ECDF(cdf.kgapScore)
  plt.plot(ecdf.x, ecdf.y)
  plt.title(f"KGAP-LINCS {args.algorithm} Score ECDF")
  plt.savefig(f"{args.odir}/KGAP-LINCS_ScoreEcdf_{args.indication_query}_{args.algorithm}.png", format="png")

  plt = ROCplotter(cdf, dcgenes, gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes, {args.algorithm}\n({args.indication_query})')
  plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_{args.indication_query}_{args.algorithm}.png", format="png")

  plt = ROCplotter(cdf, dcgenes[(dcgenes.moa)], gene_tag_r = "geneSymbol", gene_tag_v="gene", score_tag = "kgapScore", title=f'KGAP-LINCS ROC vs DrugCentral Genes (MoA), {args.algorithm}\n({args.indication_query})')
  plt.savefig(f"{args.odir}/KGAP-LINCS_ROC_{args.indication_query}_{args.algorithm}_MoA.png", format="png")
  #plt.show()

