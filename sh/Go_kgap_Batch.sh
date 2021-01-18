#!/bin/bash
#
cwd=$(pwd)
#
DATADIR="${cwd}/data"
#
queryfile="${cwd}/sh/kgap_query_list.tsv"
if [ ! -f "$queryfile" ]; then
	echo "Not found: ${queryfile}"
	exit
fi
N=$[$(cat $queryfile |wc -l) -1]
printf "KGAP queries: ${N}\n"
#
I=0
while [ $I -lt $N ]; do
	I=$[$I + 1]
	line=$(cat $queryfile |sed '1d' |sed "${I}q;d")
	IQ=$(echo "$line" |awk -F '\t' '{print $1}')
	IQ_TYPE=$(echo "$line" |awk -F '\t' '{print $2}')
	AQ=$(echo "$line" |awk -F '\t' '{print $3}')
	AQ_TYPE=$(echo "$line" |awk -F '\t' '{print $4}')
	ALGO=$(echo "$line" |awk -F '\t' '{print $5}')
	printf "Indication_query: \"${IQ}\" (${IQ_TYPE}); ATC_query: \"${AQ}\" (${AQ_TYPE}); algorithm: ${ALGO}\n"
	if [ ! "${IQ}" ]; then
		echo "No indication query; skipping."
		continue
	fi
	cmd="${cwd}/python/kgap_analysis.py --indication_query \"${IQ}\" --odir ${DATADIR}"
	if [ "${ALGO}" ]; then
		cmd="${cmd} --algorithm \"${ALGO}\""
	fi
	if [ "${IQ_TYPE}" ]; then
		cmd="${cmd} --indication_query_type \"${IQ_TYPE}\""
	fi
	if [ "${AQ}" ]; then
		cmd="${cmd} --atc_query \"${AQ}\""
	fi
	if [ "${AQ_TYPE}" ]; then
		cmd="${cmd} --atc_query_type \"${AQ_TYPE}\""
	fi
	echo "${cmd}"
	eval "${cmd}"
done
#
##
