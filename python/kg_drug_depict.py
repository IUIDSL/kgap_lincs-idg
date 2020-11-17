#!/usr/bin/env python3
"""
Check which drugs are in KG.
"""
import sys,os,json,re,logging
import pandas as pd
import requests,urllib.parse
from PIL import Image

logging.basicConfig(level=logging.INFO)

###

dcdrugs = pd.read_csv("../data/dcdrugs.tsv", "\t")
dcdrugs["pubchem_cid"] = dcdrugs["pubchem_cid"].astype(str)
logging.info("DCDRUGS n_rows: {}".format(dcdrugs.shape[0]))
logging.info("DCDRUGS PUBCHEM_CIDs: {}".format(dcdrugs['pubchem_cid'].nunique()))
logging.info("DCDRUGS columns: {}".format(str(list(dcdrugs.columns))))

###
# http://pasilla.health.unm.edu/tomcat/biocomp/mol2img?mode=cow&imgfmt=png&kekule=true&maxscale=0&maxscale=0&w=1040&h=720&smicode=NC12CC3CC%28CC%28C3%29C1%29C2

smis = dcdrugs[['smiles', 'name', 'pubchem_cid']].drop_duplicates()
smis = smis.sort_values(by = ['name'])

for i in range(smis.shape[0]):
  smi = smis['smiles'].values[i]
  name = smis['name'].values[i]
  pubchem_cid = smis['pubchem_cid'].values[i]
  smicode = urllib.parse.quote(smi)
  url = f'http://pasilla.health.unm.edu/tomcat/biocomp/mol2img?mode=cow&imgfmt=png&kekule=true&maxscale=0&maxscale=0&w=1040&h=720&smicode={smicode}'
  img = Image.open(requests.get(url, stream=True).raw)
  logging.debug("format:{}; mode:{}; size:{}".format(img.format, img.mode, img.size, img.width, img.height))
  img.info = {'name':name, 'pubchem_cid':pubchem_cid}
  #img.show()
  logging.info("{}. \"{}\" ({})".format(i+1, img.info['name'], img.info['pubchem_cid']))
  img.save("../data/dcdrugs_{:02d}_{}.png".format(i+1, name), "PNG")
  #img.thumbnail((128, 128))
  #img.save("../data/dcdrugs_{:02d}_{}.thumbnail".format(i+1, name), "PNG")

logging.info("Images: {}".format(i+1))
