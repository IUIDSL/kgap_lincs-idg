#!/bin/bash
#
cwd=$(pwd)
#
#
${cwd}/python/kgap_analysis.py \
	--indication_query "Parkinson" \
	--atc_query "NERVOUS SYSTEM" \
	--algorithm "dweighted" \
	--odir ${cwd}/data
#
${cwd}/python/kgap_analysis.py \
	--indication_query "Parkinson" \
	--atc_query "NERVOUS SYSTEM" \
	--algorithm "zweighted" \
	--odir ${cwd}/data
#
