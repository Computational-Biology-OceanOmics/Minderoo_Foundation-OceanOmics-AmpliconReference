#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

params.taxonomy_file = "../taxonomies/Fishbase_with_our_marine_families_and_Sauria_Aves_Mammalia.taxids.txt"

process RUN_12S_PIPELINE {
    publishDir "12S", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "12S/3-Final/Final_database.fasta", emit: final_db
    path "12S/3-Final/QC_Removal_stats.tsv", emit: removal_stats
    path "12S/3-Final/QC_Removal_summary_stats.tsv", emit: summary_stats
    path "12S/3-Final/Final_database_taxids.txt", emit: taxids
    path "12S/3-Final/Final_database.fasta.n*", emit: blast_db_files
    
    script:
    """
    cd 12S
    nextflow run main.nf --taxonomy_file ${taxonomy_file}
    """
}

process RUN_16S_PIPELINE {
    publishDir "16S", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "16S/3-Final/Final_database.fasta", emit: final_db
    path "16S/3-Final/QC_Removal_stats.tsv", emit: removal_stats
    path "16S/3-Final/QC_Removal_summary_stats.tsv", emit: summary_stats
    path "16S/3-Final/Final_database_taxids.txt", emit: taxids
    path "16S/3-Final/Final_database.fasta.n*", emit: blast_db_files
    
    script:
    """
    cd 16S
    nextflow run main.nf --taxonomy_file ${taxonomy_file}
    """
}

process RUN_COI_PIPELINE {
    publishDir "COI", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "COI/3-Final/Final_database.fasta", emit: final_db
    path "COI/3-Final/QC_Removal_stats.tsv", emit: removal_stats
    path "COI/3-Final/QC_Removal_summary_stats.tsv", emit: summary_stats
    path "COI/3-Final/Final_database_taxids.txt", emit: taxids
    path "COI/3-Final/Final_database.fasta.n*", emit: blast_db_files
    
    script:
    """
    cd COI
    nextflow run main.nf --taxonomy_file ${taxonomy_file}
    """
}

process RUN_MITOGENOMES_PIPELINE {
    publishDir "Mitogenomes", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "Mitogenomes/mitogenomes_fish_nuccore.renamedFiltered.fasta", emit: final_fasta
    path "Mitogenomes/mitogenomes_fish_nuccore.renamedFiltered.taxids.txt", emit: final_taxids
    
    script:
    """
    cd Mitogenomes
    nextflow run main.nf --taxonomy_file ${taxonomy_file}
    """
}

process MERGE_DATABASES {
    publishDir ".", mode: 'copy'
    
    input:
    path twelve_s_db
    path twelve_s_taxids
    path sixteen_s_db
    path sixteen_s_taxids
    path coi_db
    path coi_taxids
    path mitogenomes_fasta
    path mitogenomes_taxids
    
    output:
    path "12S.16S.COI.fasta", emit: merged_fasta
    path "12S.16S.COI.taxids.txt", emit: merged_taxids
    path "12S.16S.COI.Mitogenomes.fasta", emit: final_fasta
    path "12S.16S.COI.Mitogenomes.taxids.txt", emit: final_taxids
    path "12S.16S.COI.Mitogenomes.fasta.n*", emit: blast_db_files
    
    script:
    """
    python3 mergeDatabases.py
    """
}

workflow {
    // Input taxonomy file
    taxonomy_ch = Channel.fromPath(params.taxonomy_file)
    
    // Run all four pipelines in parallel
    RUN_12S_PIPELINE(taxonomy_ch)
    RUN_16S_PIPELINE(taxonomy_ch)
    RUN_COI_PIPELINE(taxonomy_ch)
    RUN_MITOGENOMES_PIPELINE(taxonomy_ch)
    
    // Merge databases after all pipelines complete
    MERGE_DATABASES(
        RUN_12S_PIPELINE.out.final_db,
        RUN_12S_PIPELINE.out.taxids,
        RUN_16S_PIPELINE.out.final_db,
        RUN_16S_PIPELINE.out.taxids,
        RUN_COI_PIPELINE.out.final_db,
        RUN_COI_PIPELINE.out.taxids,
        RUN_MITOGENOMES_PIPELINE.out.final_fasta,
        RUN_MITOGENOMES_PIPELINE.out.final_taxids
    )
}