#!/usr/bin/env python3
###
# Based on perturbagen.R
###

import sys,os,logging
import pandas as pd

if __name__=="__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  if (len(sys.argv) < 4):
    logging.error("4 args required, 3 input files, 1 output.")
    sys.exit(1)

  fn1 = sys.argv[1] #GSE92742_Broad_LINCS_pert_info.txt.gz
  fn2 = sys.argv[2] #GSE70138_Broad_LINCS_pert_info_2017-03-06.txt.gz
  fn3 = sys.argv[3] #GSE70138_Broad_LINCS_pert_info.txt.gz
  ofile = sys.argv[4] #perturbagen.tsv
  #
  part1 = pd.read_table(fn1, "\t", na_values=["-666", "-666.0"])#colClasses=c("character", "character", "character", "logical", "character", "character", "character", "character")
  logging.info(f"columns: {part1.columns}")
  part1 = part1.drop(columns=["is_touchstone", "inchi_key_prefix", "pubchem_cid"])
  #
  part2 = pd.read_table(fn2, "\t", na_values=["-666", "-666.0"])
  #
  part3 = pd.read_table(fn3, "\t", na_values=["-666", "-666.0"])
  part3 = part3[~part3.pert_id.isin(part2.pert_id)]
  #
  pert = pd.concat([part1, part2, part3])
  pert.drop_duplicates(subset=["pert_id"], keep="first", inplace=True)
  pert.to_csv(ofile, "\t", index=False)
