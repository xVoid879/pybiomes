import pybiomes
from pybiomes.versions import MC_1_21_1

finder = pybiomes.Finder(MC_1_21_1)
generator = pybiomes.Generator(MC_1_21_1, 0)
filter_criteria = {
    # Min x/z block coordinates of the chunk
    "pos": pybiomes.Pos(-400, 48),
    "underground": False,
    "airpocket": False,
    "giant": False,
    # 90 degrees clockwise rotation
    "rot": 1,
    # portal_1
    "type": 1,
    "mirror": True
}

for lower48 in range(1000000):
    pos = finder.get_structure_pos(pybiomes.structures.Ruined_Portal,
                                   lower48, -1, 0)
    if not pos:
        continue
    # Get the chunk seed
    rng = pybiomes.Rng(finder.chunk_generate_rnd(lower48,
                                                 pos.x >> 4,
                                                 pos.z >> 4))

    # The following logic is valid for ruined portals, except those found in
    # desert, jungle, swamp, ocean, or nether biomes. If you know your target
    # portal is notin one of those, you can use this logic to find a valid
    # structure seed, and then later just filter the world seeds that have the
    # correct biomes at this location. To modify for jungle, remove the
    # underground check, but keep the airpocket check. To modify for the
    # others, remove both underground and airpocket checks.
    underground = rng.next_float() < 0.5
    airpocket = rng.next_float()
    airpocket = underground or airpocket < 0.5
    giant = rng.next_float() < 0.05
    var = rng.next_int(3 if giant else 10) + 1
    rot = rng.next_int(4)
    mirror = rng.next_float() < 0.5
    
    # For comparing filters to actual values for this structure seed
    filters = [f for f in filter_criteria.keys() if f != 'pos']
    checks = [underground, airpocket, giant, rot, var, mirror]

    # Check if the portal matches the filter criteria
    if (pos.x == filter_criteria["pos"].x and pos.z == filter_criteria["pos"].z
        and all(value == filter_criteria[key]
                for key, value in zip(filters, checks))):
        print(lower48)
