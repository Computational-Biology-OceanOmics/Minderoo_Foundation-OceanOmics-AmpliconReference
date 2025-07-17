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

workflow {
    // Input taxonomy file
    taxonomy_ch = Channel.fromPath(params.taxonomy_file)
    
    // Run both pipelines in parallel
    RUN_12S_PIPELINE(taxonomy_ch)
    RUN_16S_PIPELINE(taxonomy_ch)
    
    // Optional: collect outputs for further processing
    // all_final_dbs = RUN_12S_PIPELINE.out.final_db.mix(RUN_16S_PIPELINE.out.final_db)
    // all_stats = RUN_12S_PIPELINE.out.removal_stats.mix(RUN_16S_PIPELINE.out.removal_stats)
}