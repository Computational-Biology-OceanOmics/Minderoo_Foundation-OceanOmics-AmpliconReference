# mamba create -n entrez -c bioconda entrez-direct -y
# conda activate entrez


# error taxa

import os
all_ids = []
init_dl_string = 'esearch -db nuccore -query \'('
init_other_dl_string = 'esearch -db gene -query \'('
with open('../../taxonomies/Fishbase_with_our_marine_families_and_Sauria_Aves_Mammalia.taxids.txt') as fh:
    for line in fh:
        ll = line.split()
        if len(ll) != 2:
            continue
        thisid = ll[-1]
        all_ids.append(thisid)
        dl_string = init_dl_string
        dl_string += f'txid{thisid}[ORGN] '

        dl_string = dl_string.rstrip('OR ') + ')' + ' AND ("cytochrome c oxidase 1"[Title] OR "cytochrome oxidase subunit I"[Title] OR COI[Title] OR COXI[Title] OR COX1[Title] OR "COX 1"[Title] OR "COX I"[Title] OR CO1[Title] OR C01[Title] OR "cytochrome oxidase I"[Title] OR "cytochrome oxidase subunit I"[Title] OR "cytochrome oxidase subunit 1"[Title] OR "cytochrome oxidase 1"[Title] OR "cytochrome c oxidase subunit I"[Title] OR "cytochrome c oxidase subunit 1"[Title]) NOT environmental sample[Title] NOT environmental samples[Title] NOT environmental[Title] NOT uncultured[Title] NOT unclassified[Title] NOT unidentified[Title] NOT unverified[Title] \' | efetch -format fasta >> c01_fish_nuccore.fasta'
        print(dl_string)
        #if thisid not in not_in_gene:
        other_dl_string = init_other_dl_string
        other_dl_string += f'txid{thisid}[ORGN] '
        other_dl_string = other_dl_string.rstrip('OR ') + ') AND ("cytochrome c oxidase 1"[Title] OR "cytochrome oxidase subunit I"[Title] OR COI[Title] OR COXI[Title] OR COX1[Title] OR "COX 1"[Title] OR "COX I"[Title] OR CO1[Title] OR C01[Title] OR "cytochrome oxidase I"[Title] OR "cytochrome oxidase subunit I"[Title] OR "cytochrome oxidase subunit 1"[Title] OR "cytochrome oxidase 1"[Title] OR "cytochrome c oxidase subunit I"[Title] OR "cytochrome c oxidase subunit 1"[Title]) AND ("source mitochondrion"[property] AND alive[prop])\' | efetch -format docsum |   xtract -pattern GenomicInfoType -element ChrAccVer ChrStart ChrStop | while IFS=$\'\\t\' read acn str stp;   do   efetch -db nuccore -format fasta  -id "$acn" -chr_start "$str" -chr_stop "$stp"; done | sed \"s/>/>CO1_/\" >> c01_fish_gene.fasta'
        print(other_dl_string)
        


#dl_string = dl_string.rstrip('OR ') + ')' + ' AND ("cytochrome c oxidase 1"[Title] OR "cytochrome oxidase subunit I"[Title] OR COI[Title] OR COXI[Title] OR COX1[Title] OR "COX 1"[Title] OR "COX I"[Title] OR CO1[Title] OR C01[Title] OR "cytochrome oxidase I"[Title] OR "cytochrome oxidase subunit I"[Title] OR "cytochrome oxidase subunit 1"[Title] OR "cytochrome oxidase 1"[Title] OR "cytochrome c oxidase subunit I"[Title] OR "cytochrome c oxidase subunit 1"[Title]) NOT environmental sample[Title] NOT environmental samples[Title] NOT environmental[Title] NOT uncultured[Title] NOT unclassified[Title] NOT unidentified[Title] NOT unverified[Title] \' | efetch -format fasta > c01_fish_nuccore.fasta'

#other_dl_string = other_dl_string.rstrip('OR ') + ') AND ("cytochrome c oxidase 1"[Title] OR "cytochrome oxidase subunit I"[Title] OR COI[Title] OR COXI[Title] OR COX1[Title] OR "COX 1"[Title] OR "COX I"[Title] OR CO1[Title] OR C01[Title] OR "cytochrome oxidase I"[Title] OR "cytochrome oxidase subunit I"[Title] OR "cytochrome oxidase subunit 1"[Title] OR "cytochrome oxidase 1"[Title] OR "cytochrome c oxidase subunit I"[Title] OR "cytochrome c oxidase subunit 1"[Title]) AND ("source mitochondrion"[property] AND alive[prop])\' | efetch -format docsum |   xtract -pattern GenomicInfoType -element ChrAccVer ChrStart ChrStop | while IFS=$\'\\t\' read acn str stp;   do   efetch -db nuccore -format fasta  -id "$acn" -chr_start "$str" -chr_stop "$stp"; done | sed \"s/>/>CO1_/\" > c01_fish_gene.fasta'
#print(dl_string)
#print(other_dl_string)

#print(dl_string)
#print(other_dl_string)
