#!/usr/bin/env python3
###
# Based on signature.R
###

import sys,os,logging
import numpy as np
import pandas as pd

if __name__=="__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  if (len(sys.argv) < 3):
    logging.error("3 file args required, LINCS sig info for GSE70138 and GSE92742, and output file.")
    sys.exit(1)

  fn1 = sys.argv[1] #GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz
  fn2 = sys.argv[2] #GSE92742_Broad_LINCS_sig_info.txt.gz
  ofile = sys.argv[3] #signature.tsv
  #
  part1 = pd.read_table(fn1, "\t", na_values=["-666", "-666.0"])
  logging.info(f"columns: {part1.columns}")
  part1 = part1[["sig_id", "pert_id", "pert_iname", "pert_type", "cell_id", "pert_idose", "pert_itime"]]
  #
  part2 = pd.read_table(fn2, "\t", na_values=["-666", "-666.0"], dtype="str")
  part2.pert_time = part2.pert_time.astype(np.int32)
  logging.info(f"columns: {part2.columns}")
  part2 = part2[["sig_id", "pert_id", "pert_iname", "pert_type", "cell_id", "pert_idose", "pert_itime"]]
  #
  sign = pd.concat([part1, part2])
  sign.drop_duplicates(subset=["sig_id"], keep="first", inplace=True)
  sign.to_csv(ofile, "\t", index=False)
