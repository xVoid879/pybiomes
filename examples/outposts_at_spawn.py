import pybiomes

from pybiomes.versions import MC_1_21_1
from pybiomes.dimensions import DIM_OVERWORLD

finder = pybiomes.Finder(MC_1_21_1)
generator = pybiomes.Generator(MC_1_21_1, 0)

for lower48 in range(10000):
    pos = finder.get_structure_pos(pybiomes.structures.Outpost, lower48, 0, 0)
    
    if not pos:
        continue

    if pos.x >= 16 or pos.z >= 16:
        continue

    for upper16 in range(10000):
        seed = lower48 | (upper16 << 48)
        generator.apply_seed(seed, DIM_OVERWORLD)

        if generator.is_viable_structure_pos(pybiomes.structures.Outpost, pos.x, pos.z, 0):
            print(seed) 