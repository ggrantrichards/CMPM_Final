#!/usr/bin/env python3
from flask import Flask, request, render_template_string, send_file, jsonify
import requests
import tempfile
import os
import time
import json
import gzip
import shutil
from collections import OrderedDict
import nbtlib
from nbtlib import tag, Compound, File

app = Flask(__name__)

# Your API key – in production, store this securely!
API_KEY = "AIzaSyCa9HhtzeMkPB4kQh3jBF2-hjLETYLZPwY"

# Hypothetical external API endpoint; if it fails, the dummy generator is used.
EXTERNAL_API_ENDPOINT = "https://gemini.googleapis.com/v1/generateLitematic"


def convert_json_to_litematic(json_file):
    import time
    import gzip
    import shutil
    from collections import OrderedDict
    import nbtlib
    from nbtlib import tag, Compound, File

    with open(json_file, "r") as f:
        data = json.load(f)

    sx, sy, sz = data["Size"]
    total_volume = sx * sy * sz
    total_blocks = sum(1 for val in data["BlockData"] if val != 0)

    # Create the region’s BlockStates and TileEntities
    blockstates = tag.ByteArray(data["BlockData"])
    tile_entities = tag.List([Compound(te) for te in data["TileEntityData"]])

    # Build a typed List of Compound for the block-state palette
    block_state_palette = tag.List[Compound]()

    for p in data["Palette"]:
        name_str = p.get("Name", "minecraft:air")
        props    = p.get("Properties", {})
        # Convert the properties to NBT-literal values
        # (If your props are always strings, you can just do tag.String(val).
        #  If some are ints/bools, handle them accordingly.)
        props_compound = Compound()
        for k, v in props.items():
            # Example: treat everything as string. Adjust as needed.
            props_compound[k] = tag.String(str(v))

        # Append the Compound to the typed List
        block_state_palette.append(Compound({
            "Name": tag.String(name_str),
            "Properties": props_compound
        }))

    # Hard-coded created time in epoch ms (2024-07-27 14:52:42)
    created_ms = 1722061962000

    # Build Metadata
    metadata = Compound({
        "EnclosingSize": tag.List([tag.Int(sx), tag.Int(sy), tag.Int(sz)]),
        "TimeCreated":   tag.Long(created_ms),
        "TimeModified":  tag.Long(created_ms),
        "Author":        tag.String(data["Author"]),
        "Name":          tag.String(data["Name"]),
        "Description":   tag.String(""),
        "RegionCount":   tag.Int(1),
        "TotalBlocks":   tag.Int(total_blocks),
        "TotalVolume":   tag.Int(total_volume),
    })

    # Single region called "Region_1"
    region_1 = Compound({
        "Position": tag.List([tag.Int(0), tag.Int(0), tag.Int(0)]),
        "Size":     tag.List([tag.Int(sx), tag.Int(sy), tag.Int(sz)]),
        "BlockStates": blockstates,
        "Entities":    tag.List(),
        "TileEntities": tile_entities,
        "PendingBlockTicks": tag.List(),
        "PendingFluidTicks": tag.List(),
    })

    # Litematica root
    litematica_root = Compound({
        "Metadata": metadata,
        "Regions": Compound({
            "Region_1": region_1
        }),
        "Version": tag.Int(6),
        "MinecraftVersion": tag.String("1.21.4"),
        "MinecraftDataVersion": tag.Int(3600),
        "DataVersion": tag.Int(3600),
        "SchemaVersion": tag.Int(3700),
        "BlockStatePalette": block_state_palette,
        "PaletteMax": tag.Int(len(block_state_palette)),
    })

    # Wrap in an NBT File with root "Litematica"
    nbt_file = File({"Litematica": litematica_root})

    # Save uncompressed first
    tmp_uncompressed = tempfile.NamedTemporaryFile(delete=False, suffix=".nbt")
    tmp_uncompressed.close()
    nbt_file.save(tmp_uncompressed.name)

    # Then gzip-compress to .litematic
    tmp_compressed = tmp_uncompressed.name + ".litematic"
    with open(tmp_uncompressed.name, 'rb') as f_in, gzip.open(tmp_compressed, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.unlink(tmp_uncompressed.name)
    return tmp_compressed
# --- Dummy schematic generator ---
def generate_dummy_schematic(prompt):
    """
    Generate a dummy schematic JSON file for a 25×25×25 structure.
    A simple house design: floor, walls, roof.
    """
    width = 25
    height = 25
    length = 25
    total = width * height * length
    block_data = [0] * total  # default air

    def within(x, low, high):
        return low <= x <= high

    # Fill BlockData in YZX order.
    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = (y * length + z) * width + x
                if y == 0:
                    if within(x, 5, 19) and within(z, 5, 19):
                        if x in [5, 19] or z in [5, 19]:
                            block_data[index] = 4  # stone_bricks
                        else:
                            block_data[index] = 1  # oak_planks
                elif 1 <= y <= 8:
                    if within(x, 5, 19) and within(z, 5, 19):
                        if x in [5, 19] or z in [5, 19]:
                            # Door gap at (x=12, z=5, y=1..2)
                            if z == 5 and x == 12 and y in [1,2]:
                                block_data[index] = 0
                            else:
                                block_data[index] = 1  # oak_planks
                elif 9 <= y <= 14:
                    if within(x, 4, 20) and within(z, 4, 20):
                        # Tiered roof with oak stairs (2) and peak of oak planks (1)
                        if y == 11 and within(x, 7, 17) and within(z, 7, 17):
                            block_data[index] = 1  # oak_planks
                        else:
                            block_data[index] = 2  # oak_stairs

    # Prepare a minimal JSON
    schematic_json = {
        "Version": 2,
        "Author": "Gemini Wrapper",
        "Name": f"{prompt} House",
        "Date": int(time.time()),
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
    tmp_path = os.path.join(tempfile.gettempdir(), "dummy_schematic.json")
    with open(tmp_path, "w") as f:
        json.dump(schematic_json, f, separators=(",", ":"), indent=2)
    return tmp_path

@app.route("/", methods=["GET"])
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gemini Schematic Generator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; }
            textarea { width: 100%; max-width: 600px; }
            input[type="submit"] { padding: 0.5em 1em; }
        </style>
    </head>
    <body>
        <h1>Gemini Schematic Generator</h1>
        <p>Enter your prompt (e.g. "Medieval castle", "Homey cabin", "Japanese") below:</p>
        <form method="POST" action="/generate">
            <label for="prompt">Prompt:</label><br>
            <textarea id="prompt" name="prompt" rows="4" placeholder="Enter your prompt here..."></textarea><br><br>
            <input type="submit" value="Generate .litematic">
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "No prompt provided."}), 400

    # Attempt the external API call
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "prompt": prompt,
        "dimensions": [25, 25, 25],
        "style": "japanese",
        "output_format": "litematic"
    }
    try:
        response = requests.post(EXTERNAL_API_ENDPOINT, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        external_success = True
    except Exception as e:
        print("External API call failed, using dummy generator:", str(e))
        external_success = False

    if external_success:
        # We got a .litematic from the external API
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".litematic")
        tmp.write(response.content)
        tmp.close()
        output_path = tmp.name
    else:
        # Fall back to the local dummy generator
        dummy_json = generate_dummy_schematic(prompt)
        output_path = convert_json_to_litematic(dummy_json)

    return send_file(output_path, as_attachment=True, download_name="GeneratedSchematic.litematic")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
