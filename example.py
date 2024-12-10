import pybiomes

from pybiomes.versions import MC_1_21_1
from pybiomes.dimensions import DIM_OVERWORLD

r = pybiomes.Range(scale=16, x=0, y=15, z=0, sx=100, sy=1, sz=100)
generator = pybiomes.Generator(MC_1_21_1, 0)
generator.apply_seed(123, DIM_OVERWORLD)

biome_ids = generator.gen_biomes(r)

# for seed in range(100000):
    # generator.apply_seed(seed, DIM_OVERWORLD)
    # biome_id = generator.get_biome_at(1, 0, 60, 0)
    # if biome_id == pybiomes.biomes.mushroom_fields:
        # print(seed)