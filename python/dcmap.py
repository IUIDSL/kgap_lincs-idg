#!/usr/bin/env python3
"""
Based on dcmap.R (formerly gen.dcmap.R).
R version used embedded Derby DrugCentral; now we use
PostgreSQL instance.
"""
###
import os,sys,re,logging,yaml
import pandas
from pandas.io.sql import read_sql_query
import psycopg2,psycopg2.extras

###
def ReadParamFile(fparam):
  params={};
  with open(fparam, 'r') as fh:
    for param in yaml.load_all(fh, Loader=yaml.BaseLoader):
      for k,v in param.items():
        params[k] = v
  return params

###
if __name__=="__main__":
  fout = open(sys.argv[1] , "w") if len(sys.argv)>2 else sys.stdout
  fout.write("UPDATE perturbagen SET dc_id = NULL, is_parent = NULL;\n")

  params = ReadParamFile(os.environ['HOME']+"/.drugcentral.yaml")
  dsn = (f"host='{params['DBHOST']}' port='{params['DBPORT']}' dbname='{params['DBNAME']}' user='{params['DBUSR']}' password='{params['DBPW']}'")
  dbcon = psycopg2.connect(dsn)
  dbcon.cursor_factory = psycopg2.extras.DictCursor

  drug_names = read_sql_query("SELECT id,name,parent_id FROM synonyms", dbcon)
  drug_inchi = read_sql_query("SELECT id,inchikey FROM structures WHERE inchikey IS NOT NULL", dbcon)
  parent_inchi = read_sql_query("SELECT cd_id id,inchikey FROM parentmol WHERE inchikey IS NOT NULL", dbcon)
  dbcon.close()

  drug_names.name = drug_names.name.str.replace("'", "''")

  d1 = drug_names[drug_names.id.notna()]

  d1["sql"] = "UPDATE perturbagen SET dc_id = " + + d1["id"].astype("str") + " WHERE LOWER('" + d1["name"] + "')=LOWER(pert_iname) AND pert_type = 'trt_cp';"
  d1.to_csv(fout, "\t", columns=["sql"], header=False, index=False)

  d2 = drug_names[(drug_names.id.isna() & drug_names.parent_id.notna())]
  d2["sql"] = "UPDATE perturbagen SET dc_id = " + d2.parent_id.astype("str") + ", is_parent=true WHERE LOWER('" + d2.name + "')=LOWER(pert_iname) AND pert_type = 'trt_cp' AND dc_id IS NULL;"
  d2.to_csv(fout, "\t", columns=["sql"], header=False, index=False)

  drug_inchi["sql"] = "UPDATE perturbagen SET dc_id = " + drug_inchi.id.astype("str") + " WHERE inchi_key='" + drug_inchi.inchikey + "' AND pert_type = 'trt_cp' AND dc_id IS NULL;"
  drug_inchi.to_csv(fout, "\t", columns=["sql"], header=False, index=False)

  parent_inchi["sql"] = "UPDATE perturbagen SET dc_id = " + parent_inchi.id.astype("str") + ", is_parent=true WHERE inchi_key='" + parent_inchi.inchikey + "' AND pert_type = 'trt_cp' AND dc_id IS NULL;"
  parent_inchi.to_csv(fout, "\t", columns=["sql"], header=False, index=False)

  fout.write("CREATE INDEX pert_drug_idx ON perturbagen(dc_id);\n")
