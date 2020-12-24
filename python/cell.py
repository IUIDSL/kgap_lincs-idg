#!/usr/bin/env python3
###
# Based on cell.R

import sys,os,logging
import pandas as pd

if __name__=="__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  if (len(sys.argv) < 2):
    logging.error("3 file args required, LINCS cell info for GSE70138 and GSE92742, and output file.")
    sys.exit(1)

  fn1 = sys.argv[1]
  fn2 = sys.argv[2]
  ofile = sys.argv[3]

  GSE70138 = pd.read_table(fn1, "\t", na_values=["-666"])
  logging.info(f"columns: {GSE70138.columns}")
  GSE70138 = GSE70138.rename(columns={
	"donor_sex":"gender",
	"primary_site":"cell_lineage",
	"subtype":"cell_histology",
	"provider_catalog_id":"cell_source_id",
	"original_source_vendor":"cell_source"})
  logging.info(f"columns: {GSE70138.columns}")

  GSE70138 = GSE70138[["cell_id", "cell_type", "cell_lineage", "cell_histology", "cell_source_id", "cell_source", "gender"]]

  #
  GSE92742 = pd.read_table(fn2, "\t", na_values=["-666"])
  GSE92742 = GSE92742.rename(columns={
	"donor_sex":"gender",
	"primary_site":"cell_lineage",
	"subtype":"cell_histology",
	"provider_catalog_id":"cell_source_id",
	"original_source_vendor":"cell_source"})
  GSE92742 = GSE92742[["cell_id", "cell_type", "cell_lineage", "cell_histology", "cell_source_id", "cell_source", "gender"]]

  #
  cells = pd.concat([GSE70138, GSE92742])
  cells.drop_duplicates(subset=["cell_id"], keep="first", inplace=True)
  cells.to_csv(ofile, "\t", index=False)
