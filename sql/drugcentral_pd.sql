SELECT DISTINCT
	ids.identifier AS pubchem_cid,
	s.id,
	s.name,
	atc.l1_code,
	atc.l1_name
FROM
	omop_relationship omop
JOIN
	structures s ON omop.struct_id = s.id
JOIN
	identifier ids ON ids.struct_id = s.id
JOIN
        struct2atc s2atc ON s2atc.struct_id = s.id
JOIN
       atc ON atc.code = s2atc.atc_code
WHERE
	ids.id_type = 'PUBCHEM_CID'
	AND atc.l1_name = 'NERVOUS SYSTEM'
	AND omop.relationship_name = 'indication'
	AND (omop.concept_name ~* 'Parkinson' OR omop.snomed_full_name ~* 'Parkinson')
ORDER BY
        s.id
	;
