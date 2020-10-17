SELECT DISTINCT
        atf.target_name,
        atf.gene,
        atf.moa
FROM
        act_table_full atf
JOIN
	structures s ON s.id = atf.struct_id
JOIN
	omop_relationship omop ON omop.struct_id = s.id
WHERE
        omop.relationship_name = 'indication'
        AND omop.concept_name ~* 'Parkinson'
;
