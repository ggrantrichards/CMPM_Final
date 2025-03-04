#!/usr/bin/env python3
import json

# Dimensions for a 25×25×25 schematic.
width = 25
height = 25
length = 25
total = width * height * length

# Palette indices:
# 0: minecraft:air
# 1: minecraft:oak_planks
# 2: minecraft:oak_stairs
# 3: minecraft:glass
# 4: minecraft:stone_bricks
# 5: minecraft:dark_oak_log
# 6: minecraft:leaves

block_data = []

def within(x, low, high):
    return low <= x <= high

# Generate BlockData in YZX order (y outer, then z, then x).
for y in range(height):
    for z in range(length):
        for x in range(width):
            val = 0  # default air

            # For demonstration, we create a simple structural framework:
            # Floor (y==0): House footprint from x=5 to 19, z=5 to 19.
            if y == 0:
                if within(x,5,19) and within(z,5,19):
                    # Border of floor uses stone_bricks (4), interior uses oak_planks (1)
                    if x == 5 or x == 19 or z == 5 or z == 19:
                        val = 4
                    else:
                        val = 1
                else:
                    val = 0
            # Walls (y 1 to 8): In the same footprint, perimeter is oak_planks (1).
            elif 1 <= y <= 8:
                if within(x,5,19) and within(z,5,19):
                    if x == 5 or x == 19 or z == 5 or z == 19:
                        # Create a door gap on front wall (z==5) at x==12 for y==1,2.
                        if z == 5 and x == 12 and y in [1,2]:
                            val = 0
                        # Use dark oak logs at the four corners.
                        elif (x, z) in [(5,5), (5,19), (19,5), (19,19)]:
                            val = 5
                        else:
                            val = 1
                    else:
                        val = 0
                else:
                    val = 0
            # Roof (y 9 to 14):
            elif 9 <= y <= 14:
                # Use stairs (2) for roof overhang covering x=4..20, z=4..20.
                if within(x,4,20) and within(z,4,20):
                    # For a tiered roof, each higher layer shrinks by one block:
                    if y == 9:
                        val = 2
                    elif y == 10 and within(x,5,19) and within(z,5,19):
                        val = 2
                    # At the peak, use oak_planks (1)
                    elif y == 11 and within(x,7,17) and within(z,7,17):
                        val = 1
                    else:
                        val = 0
                else:
                    val = 0
            # Chimney: a simple column at (18,8) from y=9 to 14.
            elif 9 <= y <= 14:
                if x == 18 and z == 8:
                    val = 5
            # Above roof: y 15 to 24, all air.
            else:
                val = 0

            block_data.append(val)

assert len(block_data) == total, f"Expected {total} block entries, got {len(block_data)}"

data = {
    "Version": 2,
    "Author": "ChatGPT",
    "Name": "Japanese House",
    "Date": 1700000000,
    "Size": [width, height, length],
    "Offset": [0, 0, 0],
    "BlockData": block_data,
    "TileEntityData": [],
    "Palette": [
        {"Name": "minecraft:air", "Properties": {}},
        {"Name": "minecraft:oak_planks", "Properties": {}},
        {"Name": "minecraft:oak_stairs", "Properties": {}},
        {"Name": "minecraft:glass", "Properties": {}},
        {"Name": "minecraft:stone_bricks", "Properties": {}},
        {"Name": "minecraft:dark_oak_log", "Properties": {}},
        {"Name": "minecraft:leaves", "Properties": {}}
    ]
}

with open("japanese_house.json", "w") as f:
    json.dump(data, f, separators=(",", ":"), indent=2)

print("Generated japanese_house.json with", len(block_data), "block entries.")
