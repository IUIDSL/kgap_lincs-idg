#!/bin/bash
###
#
cwd=$(pwd)

DATADIR=${cwd}/data

set -x

python3 -m BioClients.idg.tinx.Client search_diseases \
	--query "Parkinson" \
	--o $DATADIR/tinx_PD_diseases.tsv
#
DIDS=$(cat $DATADIR/tinx_PD_diseases.tsv |awk -F '\t' '{print $1}' |sed '1d' |perl -pe 's/\n/,/' |sed 's/,$//')
printf "DIDS: \"${DIDS}\"\n"
#
python3 -m BioClients.idg.tinx.Client get_disease_targets \
	--ids "${DIDS}" \
	--o $DATADIR/tinx_PD_targets.tsv
#
