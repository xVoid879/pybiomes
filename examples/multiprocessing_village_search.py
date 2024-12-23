"""Example script to demonstrate how to use multiprocessing to search for a
specific village location, biome, and starting piece rotation/type, as well as
several biomes for other specified coordinates. The script first searches for
the village structure at a specific location with a specific rotation and
starting piece variant. Once a structure seed with matching village is found,
the script then generates the full 64-bit world seed and checks if the biomes
at specific locations match the filter criteria.

The script demonstrates how to use the multiprocessing module to parallelize the
search for seeds across multiple CPU cores. The script creates a pool of worker
processes that can process the structure seeds in parallel. The script then
takes those valid structure seeds and creates another pool of worker processes
to generate the full 64-bit world seeds and check if the biomes match the filter
criteria. The script uses the Pool.map() method to map the process_structure_seed
function to the list of structure seeds and the Pool.imap_unordered() method to
map the process_seeds_for_structure_seed function to the list of valid structure
seeds.

The script also includes a single-threaded version of the search for comparison
purposes. The single-threaded version processes the structure seeds serially
and is used to compare the performance of the multiprocessing version.
"""
from typing import Optional
from multiprocessing import Pool
import time

import pybiomes
from pybiomes.structures import Village
from pybiomes.versions import MC_1_19_2
from pybiomes.dimensions import DIM_OVERWORLD


GENERATOR = pybiomes.Generator(MC_1_19_2, 0)
# In this example, we are searching for a village at a certain location, where
# the starting piece type and rotation are known. Additionally, we have three
# known coordinates of biomes.
FILTER_CRITERIA = {
    "village": {
        "pos": pybiomes.Pos(16, -864),
        # plains_fountain_1
        "variant": 1,
        # COUNTERCLOCKWISE_90
        "rot": 3,
        "biome": pybiomes.biomes.plains},
    "biomes": [{
            "pos": pybiomes.Pos(-137, -762),
            "biome": pybiomes.biomes.plains
        }, {
            "pos": pybiomes.Pos(-117, -777),
            "biome": pybiomes.biomes.meadow
        }, {
            "pos": pybiomes.Pos(-145, -201),
            "biome": pybiomes.biomes.meadow
        }]
}


def to_signed_64bit(value: int) -> int:
    """Converts a 64-bit unsigned integer to a signed 64-bit integer.

    Args:
        value (int): The unsigned 64-bit integer to convert.

    Returns:
        int: The signed 64-bit integer
    """
    # Ensure the value fits in 64 bits
    value &= (1 << 64) - 1
    # Check if the value is larger than the max signed 64-bit integer
    if value >= (1 << 63):
        value -= (1 << 64)
    return value


def process_structure_seed(lower48: int) -> Optional[int]:
    """Function to process a 48-bit seed and check if it contains a village
    structure at the specified location with the specified rotation and
    starting piece variant. If the village is found, the seed is returned.

    Args:
        lower48 (int): The 48-bit seed to process.

    Returns:
        int: The seed if it is valid, otherwise None.
    """
    global FILTER_CRITERIA
    global GENERATOR
    GENERATOR.apply_seed(lower48, DIM_OVERWORLD)
    finder = pybiomes.Finder(MC_1_19_2)
    pos = finder.get_structure_pos(Village, lower48, 0, -2)
    if (pos
       and pos.x == FILTER_CRITERIA["village"]["pos"].x
       and pos.z == FILTER_CRITERIA["village"]["pos"].z):
        # Get the chunk seed
        rng = pybiomes.Rng(finder.chunk_generate_rnd(lower48,
                                                     pos.x >> 4, pos.z >> 4))
        # Get village starting piece rotation
        rot = rng.next_int(4)
        # Get plains village starting piece variant. While the actual biome
        # check requires the full 64 bits, we can pre-filter the structure
        # seeds based on which roll they would get for variant. For plains
        # villages, it is a nextInt(204). Biome check will come in second
        # phase.
        var_roll = rng.next_int(204)
        if var_roll < 50:
            # plains_fountain_1
            vart = 1
        elif var_roll < 100:
            # plains_meeting_point_1
            vart = 2
        elif var_roll < 150:
            # plains_meeting_point_2
            vart = 3
        elif var_roll < 200:
            # plains_meeting_point_3
            vart = 4
        elif var_roll < 201:
            # abandoned 1
            vart = -1
        elif var_roll < 202:
            # abandoned 2
            vart = -2
        elif var_roll < 203:
            # abandoned 3
            vart = -3
        elif var_roll < 204:
            # abandoned 4
            vart = -4

        if (rot == FILTER_CRITERIA["village"]["rot"]
           and vart == FILTER_CRITERIA["village"]["variant"]):
            return lower48

    return None


def process_seed(seed: int) -> Optional[int]:
    """Function to check world seed to see if village & other biomes match
    the filter criteria. If the seed is valid, it is returned.

    Args:
        seed (int): The world seed to check.

    Returns:
        int: The seed if it is valid, otherwise None.
    """
    global FILTER_CRITERIA
    global GENERATOR
    GENERATOR.apply_seed(seed, DIM_OVERWORLD)
    # Check if village can actually spawn at the location in the world seed
    if GENERATOR.is_viable_structure_pos(Village, FILTER_CRITERIA["village"]["pos"].x, FILTER_CRITERIA["village"]["pos"].z, 0):
        # Get world biomes at the locations specified in the filter
        biomes = [GENERATOR.get_biome_at(1, c["pos"].x, 256, c["pos"].z) for c in FILTER_CRITERIA["biomes"]]
        # Check if village biome matches, as well as all additional coordinates
        if all(b == c["biome"] for b, c in zip(biomes, FILTER_CRITERIA["biomes"])):
            return seed


def process_seeds_for_structure_seed(lower48: int) -> list[int]:
    """Function to process a 48-bit seed and loop through all possible upper
    16 bits to generate a full 64-bit seed. The seed is then checked to see if
    it contains a village structure at the specified location with the specified
    rotation and starting piece variant. If the village is found, the seed is
    returned.

    Args:
        lower48 (int): The 48-bit seed to process.

    Returns:
        list: List of valid seeds for the given 48-bit seed.
    """
    valid_seeds = []
    for upper16 in range(0x10000):
        candidate = (upper16 << 48) | lower48  # Combine upper and lower bits
        if process_seed(candidate):
            valid_seeds.append(candidate)
    return valid_seeds


# Function to be used by single-threaded
def process_seeds_single(structure_seeds: list[int]) -> list[int]:
    """Single-threaded version of the function to process a list of 48-bit seeds
    and check if they contain a village structure at the specified location with
    the specified rotation and starting piece variant. If the village is found,
    the seed is returned.

    Args:
        structure_seeds (list): List of 48-bit seeds to process.

    Returns:
        list: List of valid seeds for the given 48-bit seeds.
    """
    valid_seeds = []
    for lower48 in structure_seeds:
        valid_seeds.extend(process_seeds_for_structure_seed(lower48))
    return valid_seeds


if __name__ == '__main__':
    # Set up data
    data = range(100000)
    print(f"Processing {len(data)} structure seeds.")
    # Measure execution time
    start = time.time()
    # Phase 1: Validate structure seeds
    with Pool() as pool:
        results = [num for num in pool.map(process_structure_seed, data) if num is not None]
    # Phase 2: World seed generation and biome checks
    with Pool() as pool:
        results = pool.imap_unordered(process_seeds_for_structure_seed, results)
        valid_seeds = [to_signed_64bit(item) for sublist in results for item in sublist]
    print(f"Total valid world seeds (multi): {len(valid_seeds)}")
    end = time.time()
    execution_time_multi = end - start
    # Measure execution time
    start = time.time()
    # Process seeds serially
    structure_seeds = []
    for seed in data:
        structure_seeds.append(process_structure_seed(seed))
    structure_seeds = [s for s in structure_seeds if s]
    results = process_seeds_single(structure_seeds)
    valid_seeds = [to_signed_64bit(r) for r in results if r]
    print(f"Total valid world seeds (single): {len(valid_seeds)}")
    end = time.time()
    execution_time_single = end - start

    print(f"Multiprocessing time: {execution_time_multi:.5f} seconds")
    print(f"Single-threaded time: {execution_time_single:.5f} seconds")
