# Minderoo Foundation OceanOmics amplicon databases

This repository contains the Minderoo Foundation OceanOmics amplicon databases and the code to generate them.

Currently the repository is structured into three folders: one for 12S genes, one for 16S genes, one for COI genes, and one for publicly available mitogenomes.

The final database formatted for BLAST with taxonomy IDs is in databases/12S.16S.Mitogenomes.v0.1.fasta.gz

The taxonomies/ folder contains Australian Actinopterygii + Elasmobranchii + Aves + Sauria + Mammalia families, and all marine fish families via fishbase. We first started out wanting only Australian families but then expanded that for deep sea work, so the download and QC scripts now take all marine familis.


# Nextflow

I used Claude Code to move all of the logic into a nextflow pipeline.

Navigate into databases/, and run 

    nextflow main.nf

which should run everything.

# Scripts

- getAssemblies.py - for each 12S, 16S, and COI. Writes an entrez script that downloads 12S, 16S, and COI sequences for sharks, bony fish, marine mammals, birds, and reptiles. The equivalent in the mitogenomes folder downloads entire genomes.
- doAllQC.py - self-blasts the genes and writes out potential mislabels and contaminants to build a final BLAST-formatted database with taxonomy IDs.
- mergeDatabases.py - builds a final BLAST database of the three folders. Removes duplicates like voucher sequences that contain a 12S, a 16S, or a COI gene.
- getFishbaseFamilies.R - this pulls out the family names of marine fish species via rfishbase

All larger files have been gzipped.
