import json
import os
from gemini_api import generate_build_with_gemini
from datetime import datetime

def generate_build(size, description):
    # Call Gemini API (or use dummy generator if needed)
    layers = generate_build_with_gemini(size, description)

    # Load block abbreviations
    with open('data/block_abbreviations.json', 'r') as f:
        block_abbreviations = json.load(f)

    # Create a unique folder for this build. Sanitize the description for folder naming.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_description = "".join(c for c in description if c.isalnum() or c in ['-', '_']).lower()
    build_folder = f"output/{safe_description}_{size}x{size}_{timestamp}"
    os.makedirs(build_folder, exist_ok=True)

    # Save each layer as a text file in the build folder
    for i, layer in enumerate(layers):
        with open(f'{build_folder}/layer_{i}.txt', 'w') as f:
            for row in layer:
                # Replace block abbreviations with their full names from block_abbreviations
                full_row = [block_abbreviations.get(block, block) for block in row]
                f.write(' '.join(full_row) + '\n')

    print(f"Build generated with size {size}x{size} and description '{description}'. Files saved in {build_folder}.")
