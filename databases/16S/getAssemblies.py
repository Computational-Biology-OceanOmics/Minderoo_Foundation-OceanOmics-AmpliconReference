# mamba create -n entrez -c bioconda entrez-direct -y
import sys
# conda activate entrez


# error taxa

# too many erroneous (non-existing!) tax ids make esearch stop.
# these are the 31/08/2022 taxids not in Gene:
not_in_gene = 'txid88651[ORGN], txid241819[ORGN], txid990930[ORGN], txid178227[ORGN], txid82890[ORGN], txid172132[ORGN], txid1489833[ORGN], txid178230[ORGN], txid1489942[ORGN], txid582432[ORGN], txid412621[ORGN], txid215353[ORGN], txid1489924[ORGN], txid117924[ORGN], txid82793[ORGN], txid57768[ORGN], txid178225[ORGN], txid270598[ORGN], txid1545868[ORGN], txid390325[ORGN], txid7832[ORGN], txid630724[ORGN], txid172143[ORGN], txid1545873[ORGN], txid172114[ORGN], txid443779[ORGN], txid2800422[ORGN], txid178224[ORGN], txid31099[ORGN], txid117842[ORGN], txid117889[ORGN], txid172118[ORGN], txid97158[ORGN], txid130262[ORGN], txid30847[ORGN], txid390344[ORGN], txid81371[ORGN], txid30758[ORGN], txid908954[ORGN], txid274689[ORGN], txid172126[ORGN], txid428447[ORGN], txid117915[ORGN], txid1213740[ORGN], txid509847[ORGN], txid178226[ORGN], txid390366[ORGN], txid210573[ORGN], txid206137[ORGN], txid490375[ORGN], txid112726[ORGN], txid1490017[ORGN], txid160493[ORGN], txid172135[ORGN], txid81387[ORGN], txid30885[ORGN], txid172121[ORGN], txid274712[ORGN], txid473342[ORGN], txid722446[ORGN], txid1489881[ORGN], txid57771[ORGN], txid40662[ORGN], txid81374[ORGN], txid2025516[ORGN], txid760215[ORGN], txid43314[ORGN]'.replace('txid','').replace('[ORGN]','').split(', ')


if len(sys.argv) != 2:
    print("Usage: python getAssemblies.py <taxonomy_file_path>", file=sys.stderr)
    sys.exit(1)

taxonomy_file_path = sys.argv[1]

import os
all_ids = []
init_dl_string = 'esearch -db nuccore -query "('
init_other_dl_string = 'esearch -db gene -query "('

with open(taxonomy_file_path) as fh:
    for line in fh:
        ll = line.split()
        if len(ll) != 2:
            continue
        thisid = ll[-1]
        all_ids.append(thisid)
        dl_string = init_dl_string
        dl_string += f'txid{thisid}[ORGN] OR '
        #if thisid not in not_in_gene:
        #    other_dl_string += f'txid{thisid}[ORGN] OR '
        dl_string = dl_string.rstrip('OR ') + ')' + ' AND (Small subunit [Title] OR 16S[Title] OR 16S ribosomal RNA[Title] OR 16S rRNA[Title]) AND (mitochondrion[Filter] OR plastid[Filter]) NOT environmental sample[Title] NOT environmental samples[Title] NOT environmental[Title] NOT uncultured[Title] NOT unclassified[Title] NOT unidentified[Title] NOT unverified[Title] " | efetch -format fasta >> 16S_fish_nuccore.fasta'
        other_dl_string = init_other_dl_string
        other_dl_string += f'txid{thisid}[ORGN] OR '
        other_dl_string = other_dl_string.rstrip('OR ') + ') AND (Small subunit [Title] OR 16S[Title])  AND ("source mitochondrion"[property] AND alive[prop])" | efetch -format docsum |   xtract -pattern GenomicInfoType -element ChrAccVer ChrStart ChrStop | while IFS=$\'\\t\' read acn str stp;   do  efetch -db nuccore -format fasta  -id "$acn" -chr_start "$str" -chr_stop "$stp"; done | sed "s/>/>16S_/" >> 16S_fish_gene.fasta'
        #print(dl_string)
        print(dl_string)
        print(other_dl_string)
        #print(os.popen(dl_string).read())



        #esearch -db nuccore -query "txid7898[ORGN] AND (16S[Title] OR 16S ribosomal RNA[Title] OR 16S rRNA[Title]) AND (mitochondrion[Filter] OR plastid[Filter]) NOT environmental sample[Title] NOT environmental samples[Title] NOT environmental[Title] NOT uncultured[Title] NOT unclassified[Title] NOT unidentified[Title] NOT unverified[Title] " | efetch -format fasta > 16S_fish.fasta

        #esearch -db nuccore -query "txid7777[ORGN] AND (16S[Title] OR 16S ribosomal RNA[Title] OR 16S rRNA[Title]) AND (mitochondrion[Filter] OR plastid[Filter]) NOT environmental sample[Title] NOT environmental samples[Title] NOT environmental[Title] NOT uncultured[Title] NOT unclassified[Title] NOT unidentified[Title] NOT unverified[Title] " | efetch -format fasta >> 16S_fish.fasta
