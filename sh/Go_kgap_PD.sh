#!/bin/bash
#
cwd=$(pwd)
#
#
${cwd}/python/ROC_analysis.py \
	--indication_query "Parkinson" \
	--atc_query "NERVOUS SYSTEM" \
	--odir ${cwd}/data
#
