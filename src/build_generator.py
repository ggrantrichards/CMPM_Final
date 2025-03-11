import json
import os
from gemini_api import generate_build_with_gemini
from datetime import datetime
import mcschematic

def generate_build(size, description, build_type="default_type"):
    # Generate layers using the Gemini API.
    layers = generate_build_with_gemini(size, build_type, description)
    
    # Load block abbreviations.
    with open('data/block_abbreviations.json', 'r') as f:
        block_abbreviations = json.load(f)
    
    # Create a unique folder for this build.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_description = "".join(c for c in description if c.isalnum() or c in ['-', '_']).lower()
    build_folder = os.path.join("..", "output", f"{safe_description}_{size}x{size}_{timestamp}")
    os.makedirs(build_folder, exist_ok=True)
    
    # Save each layer as a text file in the build folder.
    for i, layer in enumerate(layers):
        with open(os.path.join(build_folder, f'layer_{i}.txt'), 'w') as f:
            for row in layer:
                f.write(' '.join(row) + '\n')
        yield int((i + 1) / len(layers) * 100)  # Yield progress

    # Create a schematic file using mcschematic
    schem = mcschematic.MCSchematic()

    # Convert the layers into blocks in the schematic
    for z, layer in enumerate(layers):
        for y, row in enumerate(layer):
            for x, block_abbr in enumerate(row):
                block_name = block_abbreviations.get(block_abbr, "minecraft:air")  # Default to air if abbreviation is not found
                schem.setBlock((x, z, y), block_name)  # (x, z, y) for Minecraft coordinates

    # Save the schematic file
    schem.save(build_folder, f"{build_type}_{size}x{size}_{timestamp}", mcschematic.Version.JE_1_18_2)

    print(f"Build generated with {size}x{size} size and type {build_type}. Files saved in {build_folder}.")
    yield 100  # Ensure progress is 100% at the end