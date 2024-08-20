library(rfishbase)
all_species <- species()
all_families <- fb_tbl('FAMILIES')
all_species_f <- all_species %>% left_join(all_families, by = 'FamCode')
all_marine_species <- all_species_f %>% filter(Saltwater == 1)
all_marine_families <- all_marine_species$Family %>% unique()

all_marine_families %>% write.csv(file='Fishbase_marine_families.txt')
