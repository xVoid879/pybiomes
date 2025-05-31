import pybiomes
from pybiomes.versions import MC_1_16_5
from pybiomes.dimensions import DIM_NETHER

CHUNK_X = 0
CHUNK_Z = 0
FEATURE_SALT = 80003

def get_feature_seed(world_seed, chunk_x, chunk_z, salt):
    return (world_seed + (chunk_x * 341873128712) + (chunk_z * 132897987541) + salt) & ((1 << 64) - 1)

class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)
    def nextInt(self, bound):
        if (bound & (bound - 1)) == 0:
            return (bound * self.next(31)) >> 31
        while True:
            bits = self.next(31)
            val = bits % bound
            if bits - val + (bound - 1) >= 0:
                return val

def fungus_has_stem_height_24(feature_seed):
    rnd = JavaRandom(feature_seed & ((1 << 48) - 1))
    
    # Mth.nextInt(random, 4, 13) → returns value between 4 and 13 inclusive
    n2 = rnd.nextInt(10) + 4  # nextInt(10) gives 0–9, then +4 = 4–13
    
    # 1 in 12 chance of doubling
    if rnd.nextInt(12) == 0:
        n2 *= 2

    return n2 == 24

def main():
    generator = pybiomes.Generator(MC_1_16_5, 0)
    
    for seed in range(100000):
        generator.apply_seed(seed, DIM_NETHER)
        
        biome_id = generator.get_biome_at(CHUNK_X * 16 + 8, 0, CHUNK_Z * 16 + 8, 0)
        if biome_id != pybiomes.biomes.warped_forest:
            continue
        
        feature_seed = get_feature_seed(seed, CHUNK_X, CHUNK_Z, FEATURE_SALT)
        
        if fungus_has_stem_height_24(feature_seed):
            print(f"Seed {seed} has warped fungus in chunk (0,0) with stem height 24")

if __name__ == "__main__":
    main()
