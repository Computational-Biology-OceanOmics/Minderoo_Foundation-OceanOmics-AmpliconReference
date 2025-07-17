#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

params.taxonomy_file = "../../taxonomies/Fishbase_with_our_marine_families_and_Sauria_Aves_Mammalia.taxids.txt"
params.output_dir = "."

process GENERATE_DOWNLOAD_SCRIPTS {
    publishDir "${params.output_dir}", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "downloadAssemblies.sh"
    
    script:
    """
    python ${projectDir}/getAssemblies.py ${taxonomy_file} > downloadAssemblies.sh
    """
}

process DOWNLOAD_ASSEMBLIES {
    conda 'entrez.yml'
    publishDir "${params.output_dir}", mode: 'copy'
    
    input:
    path download_script
    
    output:
    path "16S_fish_gene.fasta"
    path "16S_fish_nuccore.fasta"
    
    script:
    """
    bash ${download_script}
    """
}

process CLEANUP_DIRS {
    input:
    val trigger
    
    script:
    """
    rm -rf 0-taxoncheck 1-selfblast 2-LCAs 3-Final
    """
}

process MERGE_FASTA {
    input:
    path gene_fasta
    path nuccore_fasta
    
    output:
    path "16S_fish_gene_and_nuccore.fasta"
    
    script:
    """
    cat ${gene_fasta} ${nuccore_fasta} > 16S_fish_gene_and_nuccore.fasta
    """
}

process QC_PIPELINE {
    conda 'entrez.yml'
    publishDir "${params.output_dir}", mode: 'copy'
    
    input:
    path merged_fasta
    
    output:
    path "3-Final/Final_database.fasta", emit: final_db
    path "3-Final/QC_Removal_stats.tsv", emit: removal_stats
    path "3-Final/QC_Removal_summary_stats.tsv", emit: summary_stats
    path "3-Final/Final_database_taxids.txt", emit: taxids
    path "3-Final/Final_database.fasta.n*", emit: blast_db_files
    
    script:
    """
    python ${projectDir}/doAllQC.py -i ${merged_fasta}
    """
}
// Check if pipeline was run recently (within 4 weeks)
db_file = file("${params.output_dir}/3-Final/Final_database.fasta")

if (db_file.exists()) {
long file_age_days = (System.currentTimeMillis() - db_file.lastModified()) / (1000 * 60 * 60 * 24)
if (file_age_days < 28) {
    println "Pipeline was run ${file_age_days} days ago. Skipping execution (threshold: 28 days)."
    return
}
}

 
workflow {
    // Input taxonomy file
    taxonomy_ch = Channel.fromPath(params.taxonomy_file)
    
    // Generate download scripts
    download_script = GENERATE_DOWNLOAD_SCRIPTS(taxonomy_ch)
    
    // Download assemblies
    (gene_fasta, nuccore_fasta) = DOWNLOAD_ASSEMBLIES(download_script)
    
    // Clean up directories
    CLEANUP_DIRS(download_script)
    
    // Merge FASTA files
    merged_fasta = MERGE_FASTA(gene_fasta, nuccore_fasta)
    
    // Run QC pipeline
    QC_PIPELINE(merged_fasta)
}
