#!/bin/bash
#
cwd=$(pwd)
#
#
${cwd}/python/kgap_analysis.py \
	--indication_query "Parkinson" \
	--atc_query "NERVOUS SYSTEM" \
	--odir ${cwd}/data
#
