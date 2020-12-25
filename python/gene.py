#!/usr/bin/env python3
###
# Based on gene.R
###

import sys,os,logging,re
import pandas as pd

if __name__=="__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

  if (len(sys.argv) < 3):
    logging.error("1+ input and 1 output file arguments required.")
    sys.exit(1)

  ofile = sys.argv[-1]

  genes = pd.DataFrame()

  for fn in sys.argv[1:-1]:
    logging.info(fn)
    if re.match(".*landmark.txt.gz$", fn):
      genes_this = pd.read_table(fn, "\t")
      genes_this["pr_is_lm"] = 1
    else:
      genes_this = pd.read_table(fn, "\t", usecols=["pr_gene_id", "pr_gene_symbol", "pr_gene_title", "pr_is_lm", "pr_is_bing"])

    genes = pd.concat([genes, genes_this])

  genes.drop_duplicates(subset=["pr_gene_id"], inplace=True)
  genes.to_csv(ofile, "\t", index=False)
