import pybiomes

from pybiomes.versions import MC_1_21_1

finder = pybiomes.Finder(MC_1_21_1)
sconfig =  = finder.get_structure_config(pybiomes.structures.Village)

print(sconfig)

# Should return:
# {'salt': 10387312,
#  'regionSize': 34,
#  'chunkRange': 26,
#  'structType': 5,
#  'dim': 0,
#  'rarity': 0.0}
