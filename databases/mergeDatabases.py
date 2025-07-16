from Bio import SeqIO
import os
import gzip
from collections import Counter

# Parse gzipped fasta files
with gzip.open('12S/3-Final/Final_database.fasta.gz', 'rt') as f:
    twelve = [x.id for x in SeqIO.parse(f, 'fasta')]

with gzip.open('16S/3-Final/Final_database.fasta.gz', 'rt') as f:
    sixteen = [x.id for x in SeqIO.parse(f, 'fasta')]

with gzip.open('COI/3-Final/Final_database.fasta.gz', 'rt') as f:
    coi = [x.id for x in SeqIO.parse(f, 'fasta')]

# Read taxids (assuming these are still plain text files)
taxids = {}
for line in open('12S/3-Final/Final_database_taxids.txt'):
    ll = line.split()
    name, taxid = ll
    taxids[name] = taxid

for line in open('16S/3-Final/Final_database_taxids.txt'):
    ll = line.split()
    name, taxid = ll
    taxids[name] = taxid

for line in open('COI/3-Final/Final_database_taxids.txt'):
    ll = line.split()
    name, taxid = ll
    taxids[name] = taxid

c = Counter(twelve + sixteen + coi)
dups = set()
for i in c:
    if c[i] != 1:
        dups.add(i)

with open('12S.16S.COI.fasta', 'w') as out, \
        open('12S.16S.COI.taxids.txt', 'w') as taxout:
    
    # Process 12S sequences
    with gzip.open('12S/3-Final/Final_database.fasta.gz', 'rt') as f:
        for t in SeqIO.parse(f, 'fasta'):
            if t.id in dups and t.id.startswith('NC'):
                # keep this but rename
                old_id = t.id
                t.id = '12S_' + t.id
                t.description = '12S_' + t.description
                t.name = '12S_' + t.name
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[old_id]}\n')
            elif t.id in dups and not t.id.startswith('NC'):
                # keep this - it has 12S and 16S together
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[t.id]}\n')
            else:
                oldid = t.id
                if t.id.startswith('NC'):
                    # avoid duplication with whole mitogenomes
                    t.id = '12S_%s' % (t.id)
                # not a duplicate, keep
                taxout.write(f'{t.id} {taxids[oldid]}\n')
                out.write(t.format('fasta'))
    
    # Process 16S sequences
    with gzip.open('16S/3-Final/Final_database.fasta.gz', 'rt') as f:
        for t in SeqIO.parse(f, 'fasta'):
            if t.id in dups and t.id.startswith('NC'):
                # keep this but rename
                old_id = t.id
                t.id = '16S_' + t.id
                t.description = '16S_' + t.description
                t.name = '16S_' + t.name
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[old_id]}\n')
            elif t.id in dups and not t.id.startswith('NC'):
                # skip this - we kept it with 12S
                continue
            else:
                # not a duplicate, keep
                oldid = t.id
                if t.id.startswith('NC'):
                    t.id = '16S_%s' % (t.id)
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[oldid]}\n')
    
    # Process COI sequences
    with gzip.open('COI/3-Final/Final_database.fasta.gz', 'rt') as f:
        for t in SeqIO.parse(f, 'fasta'):
            if t.id in dups and t.id.startswith('NC'):
                # keep this but rename
                old_id = t.id
                t.id = 'COI_' + t.id
                t.description = 'COI_' + t.description
                t.name = 'COI_' + t.name
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[old_id]}\n')
            elif t.id in dups and not t.id.startswith('NC'):
                # skip this - we kept it with 12S or 16S
                continue
            else:
                # not a duplicate, keep
                oldid = t.id
                if t.id.startswith('NC') or t.id.startswith('MG'):
                    t.id = 'COI_%s' % (t.id)
                out.write(t.format('fasta'))
                taxout.write(f'{t.id} {taxids[oldid]}\n')

# Combine files and create blast database
os.popen('cat 12S.16S.COI.taxids.txt Mitogenomes/mitogenomes_fish_nuccore.renamedFiltered.taxids.txt > 12S.16S.COI.Mitogenomes.taxids.txt').read()
os.popen('cat 12S.16S.COI.fasta Mitogenomes/mitogenomes_fish_nuccore.renamedFiltered.fasta > 12S.16S.COI.Mitogenomes.fasta').read()
os.popen('makeblastdb -dbtype nucl -in 12S.16S.COI.Mitogenomes.fasta -parse_seqids -taxid_map 12S.16S.COI.Mitogenomes.taxids.txt').read()
