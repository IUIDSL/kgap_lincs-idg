SELECT DISTINCT
        tc.geneid,
        tc.gene,
        tc.accession,
        tc.name,
        td.id target_id,
        td.name,
        td.target_class,
        td.protein_type,
        atf.moa,
        moat.action_type,
        atf.relation,
        atf.act_type,
        ref_act.pmid pmid_act,
        ref_act.title title_act,
        ref_act.journal journal_act,
        ref_act.dp_year dp_year_act,
        ref_moa.pmid pmid_moa,
        ref_moa.title title_moa,
        ref_moa.journal journal_moa,
        ref_moa.dp_year dp_year_moa
FROM
        structures s
        JOIN act_table_full atf ON atf.struct_id = s.id
        JOIN target_dictionary td ON td.id = atf.target_id
        JOIN td2tc ON td2tc.target_id = td.id
        JOIN target_component tc ON tc.id = td2tc.component_id
        JOIN omop_relationship omop ON omop.struct_id = s.id
        LEFT JOIN action_type moat ON moat.id = atf.moa
        LEFT JOIN reference ref_act ON ref_act.id = atf.act_ref_id
        LEFT JOIN reference ref_moa ON ref_moa.id = atf.moa_ref_id
WHERE
        omop.relationship_name = 'indication'
        AND omop.concept_name ~* 'Parkinson'
        AND (ref_act.pmid IS NOT NULL OR ref_moa.pmid IS NOT NULL)
ORDER BY
        tc.geneid
;
