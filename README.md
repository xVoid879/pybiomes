# pybiomes
Python bindings for cubiomes

# installation

Tested on Linux, but should work fine on Windows.

```bash
git clone https://github.com/ScriptLineStudios/pybiomes --recursive
pip install -e .
```

# examples

Searching for mushroom islands.
```python
import pybiomes

from pybiomes.versions import MC_1_21_1
from pybiomes.dimensions import DIM_OVERWORLD

generator = pybiomes.Generator(MC_1_21_1, 0)

for seed in range(100000):
    generator.apply_seed(seed, DIM_OVERWORLD)
    biome_id = generator.get_biome_at(1, 0, 60, 0)
    if biome_id == pybiomes.biomes.mushroom_fields:
        print(seed)
```

Searching for outposts.
```python
import pybiomes

from pybiomes.versions import MC_1_21_1
from pybiomes.dimensions import DIM_OVERWORLD

finder = pybiomes.Finder(MC_1_21_1)
generator = pybiomes.Generator(MC_1_21_1, 0)

for lower48 in range(1000000):
    pos = finder.get_structure_pos(pybiomes.structures.Outpost, lower48, 0, 0)
    
    if not pos:
        continue

    if pos.x >= 16 or pos.z >= 16:
        continue

    for upper16 in range(0x10000):
        seed = lower48 | (upper16 << 48)
        generator.apply_seed(seed, DIM_OVERWORLD)

        if generator.is_viable_structure_pos(pybiomes.structures.Outpost, pos.x, pos.z, 0):
            print(seed) 
            exit()
```
