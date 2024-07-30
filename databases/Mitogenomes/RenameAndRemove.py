from Bio import SeqIO
import os

#os.popen('grep ">" mitogenomes_fish_nuccore.fasta | cut -f 1 -d " " > names.txt').read()
#os.popen(f'cat names.txt | efetch -db nuccore -format docsum | xtract -pattern DocumentSummary -element AccessionVersion,TaxId,Organism > efetch_names_taxids.txt').read()

taxid_dict = {}
for line in open('efetch_names_taxids.txt'):
    ll = line.rstrip().split('\t')
    seq, taxid, species = ll
    taxid_dict[seq] = (taxid, species)

with open('mitogenomes_fish_nuccore.renamedFiltered.fasta', 'w') as out1, open('mitogenomes_fish_nuccore.renamedFiltered.taxids.txt', 'w') as out2:
    for seq in SeqIO.parse('mitogenomes_fish_nuccore.fasta', 'fasta'):
        if ' sp. ' in seq.description or \
                ' aff. ' in seq.description or \
                ' x ' in seq.description:
            continue
        thisid = seq.id
        thistaxid, thisspecies = taxid_dict[thisid]
        # now let's reformat the name of this.
        # old name: NCBI ID {SPACE} All info we have
        # new name: NCBI ID {SPACE} Taxonomy ID { SPACE } Species {SPACE} All info we have
        newid = f'{seq.id} {thistaxid} {thisspecies} {seq.name}'
        seq.id = newid
        out1.write(seq.format('fasta'))
        out2.write(f'{thisid} {thistaxid}\n')
