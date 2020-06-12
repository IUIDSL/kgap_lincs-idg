#!/bin/bash
###
# DrugCentral queries for Parkinson's Disease and related.
# https://github.com/jeremyjyang/BioClients
#
python3 -m BioClients.drugcentral.Client list_indications \
	--o dc_indications.tsv
#
python3 -m BioClients.drugcentral.Client search_indications \
	--ids "Parkinson" \
	--o dc_indications_PD.tsv
cat dc_indications_PD.tsv |sed -e '1d' \
	|awk -F '\t' '{print $1}' |sort -u \
	>dc_indications_PD.concept_id
#
python3 -m BioClients.drugcentral.Client get_indication_structures \
	--i dc_indications_PD.concept_id \
	--o dc_structures_PD.tsv
cat dc_structures_PD.tsv |sed -e '1d' \
	|awk -F '\t' '{print $5 "\t" $3 "\t" $4}' |sort -u \
	>dc_structures_PD.smiles
cat dc_structures_PD.smiles \
	|awk -F '\t' '{print $2}' \
	>dc_structures_PD.struct_id
#
python3 -m BioClients.drugcentral.Client get_structure_ids \
	--i dc_structures_PD.struct_id \
	--o dc_structure_ids_PD.tsv
#
python3 -m BioClients.drugcentral.Client get_structure_atcs \
	--i dc_structures_PD.struct_id \
	--o dc_structure_atcs_PD.tsv
#
