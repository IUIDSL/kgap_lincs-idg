#!/bin/bash
#
cwd=$(pwd)
#
#
${cwd}/python/kgap_analysis.py \
	--indication_query "Parkinson" --indication_query_type "substring" \
	--atc_query "NERVOUS SYSTEM" --atc_query_type "exact" \
	--algorithm "dweighted" \
	--odir ${cwd}/data
#
${cwd}/python/kgap_analysis.py \
	--indication_query "Parkinson" --indication_query_type "substring" \
	--atc_query "NERVOUS SYSTEM" --atc_query_type "exact" \
	--algorithm "zweighted" \
	--odir ${cwd}/data
#
