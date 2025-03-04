#!/usr/bin/env python3
import json
import nbtlib
from nbtlib import tag, Compound, File

def convert_to_nbt(value):
    """Recursively convert Python values to NBT tags."""
    if isinstance(value, dict):
        return Compound({k: convert_to_nbt(v) for k, v in value.items()})
    elif isinstance(value, list):
        return tag.List([convert_to_nbt(item) for item in value])
    elif isinstance(value, int):
        return tag.Int(value)
    elif isinstance(value, float):
        return tag.Float(value)
    elif isinstance(value, str):
        return tag.String(value)
    else:
        return value

input_filename = "input_build.json"
output_filename = "Japanese_House.litematic"

with open(input_filename, "r") as f:
    data = json.load(f)

nbt_data = Compound({
    "Name": tag.String(data["Name"]),
    "Author": tag.String(data["Author"]),
    "Created": tag.String("2024-07-27 14:52:42"),
    "LitematicVersion": tag.Int(6),
    "MinecraftVersion": tag.String("1.20.4"),
    "SchemaVersion": tag.Int(37001),
    "Date": tag.Long(data["Date"]),
    "Size": tag.List([tag.Int(x) for x in data["Size"]]),
    "Offset": tag.List([tag.Int(x) for x in data["Offset"]]),
    "BlockData": tag.ByteArray(data["BlockData"]),
    "TileEntityData": tag.List([convert_to_nbt(te) for te in data["TileEntityData"]]),
    "Palette": tag.List([convert_to_nbt(p) for p in data["Palette"]])
})

# Create the NBT file with a root name of "Litematica"
nbt_file = File(nbt_data, root_name="Litematica")

nbt_file.save(output_filename)
print(f"Converted {input_filename} to {output_filename}")
