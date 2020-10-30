SELECT DISTINCT
        atf.moa,
        moat.action_type,
        atf.relation,
        atf.act_type,
        td.id "target_id",
        td.name,
        td.target_class,
        td.protein_type,
        tc.gene,
        tc.geneid,
        tc.accession,
        tc.name,
        ref.pmid,
        ref.title,
        ref.journal,
        ref.dp_year
FROM
        structures s
        JOIN act_table_full atf ON atf.struct_id = s.id
        JOIN target_dictionary td ON td.id = atf.target_id
        JOIN td2tc ON td2tc.target_id = td.id
        JOIN target_component tc ON tc.id = td2tc.component_id
        JOIN action_type moat ON moat.id = atf.moa
        JOIN omop_relationship omop ON omop.struct_id = s.id
        JOIN reference ref ON ref.id = atf.act_ref_id
WHERE
        atf.moa IS NOT NULL
        AND omop.relationship_name = 'indication'
        AND omop.concept_name ~* 'Parkinson'
;