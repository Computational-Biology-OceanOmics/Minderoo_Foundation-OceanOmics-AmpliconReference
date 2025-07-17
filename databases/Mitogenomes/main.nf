#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

params.taxonomy_file = "../../taxonomies/Fishbase_with_our_marine_families_and_Sauria_Aves_Mammalia.taxids.txt"
params.output_dir = "."

process DOWNLOAD_MITOGENOMES {
    conda 'entrez.yml'
    publishDir "${params.output_dir}", mode: 'copy'
    
    input:
    path taxonomy_file
    
    output:
    path "mitogenomes_fish_nuccore.fasta"
    path "names.txt"
    path "efetch_names_taxids.txt"
    
    script:
    """
    python ${projectDir}/getAssemblies.py
    """
}

process RENAME_AND_FILTER {
    conda 'entrez.yml'
    publishDir "${params.output_dir}", mode: 'copy'
    
    input:
    path fasta_file
    path names_file
    path taxids_file
    
    output:
    path "mitogenomes_fish_nuccore.renamedFiltered.fasta", emit: final_fasta
    path "mitogenomes_fish_nuccore.renamedFiltered.taxids.txt", emit: final_taxids
    
    script:
    """
    python ${projectDir}/RenameAndRemove.py
    """
}

workflow {
    // Check if pipeline was run recently (within 4 weeks)
    final_fasta_file = file("${params.output_dir}/mitogenomes_fish_nuccore.renamedFiltered.fasta")
    
    if (final_fasta_file.exists()) {
        long file_age_days = (System.currentTimeMillis() - final_fasta_file.lastModified()) / (1000 * 60 * 60 * 24)
        if (file_age_days < 28) {
            println "Pipeline was run ${file_age_days} days ago. Skipping execution (threshold: 28 days)."
            return
        }
    }
    
    // Input taxonomy file
    taxonomy_ch = Channel.fromPath(params.taxonomy_file)
    
    // Download mitogenomes
    (fasta_file, names_file, taxids_file) = DOWNLOAD_MITOGENOMES(taxonomy_ch)
    
    // Rename and filter sequences
    RENAME_AND_FILTER(fasta_file, names_file, taxids_file)
}