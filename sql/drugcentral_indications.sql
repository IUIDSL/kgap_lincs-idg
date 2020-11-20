SELECT DISTINCT
	omop.concept_id omop_concept_id,
	omop.concept_name omop_concept_name,
	omop.umls_cui,
	COUNT(s.id) drug_count
FROM
	omop_relationship omop
JOIN
	structures s ON omop.struct_id = s.id
WHERE
	omop.relationship_name = 'indication'
	AND omop.umls_cui IS NOT NULL
GROUP BY
        omop.concept_id,
	omop.concept_name,
	omop.umls_cui
ORDER BY drug_count DESC
	;