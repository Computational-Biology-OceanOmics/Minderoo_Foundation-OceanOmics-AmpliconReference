fishbase = set([x.rstrip() for x in open('Fishbase_marine_families.txt')])
ours = set([x.rstrip() for x in open('Australian_families.txt')])

#print(', '.join(sorted(list(fishbase - ours))))
print('\n'.join(sorted(list(ours - fishbase))))
