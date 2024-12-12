import pybiomes

from pybiomes.versions import MC_1_21_1
from pybiomes.dimensions import DIM_OVERWORLD

generator = pybiomes.Generator(MC_1_21_1, 0)

for seed in range(100000):
    generator.apply_seed(seed, DIM_OVERWORLD)
    biome_id = generator.get_biome_at(1, 0, 60, 0)
    if biome_id == pybiomes.biomes.mushroom_fields:
        print(seed)