import json
import os
from gemini_api import generate_build_with_gemini
from datetime import datetime
import mcschematic
from genetic_algorithm import GeneticAlgorithm

def validate_block_structure(layers):
    # Ensure that the block structure is valid and does not contain lists within blocks
    for layer in layers:
        for row in layer:
            for block in row:
                if isinstance(block, list):
                    return False  # Invalid structure if block is a list
    return True  # Valid structure

def generate_build(size, description, build_type="default_type"):
    # Generate layers using the Gemini API.
    try:
        build, allowed_blocks = generate_build_with_gemini(size, build_type, description)
        print(f"Initial build from Gemini API: {json.dumps(build, indent=2)}")
        print(f"Allowed blocks from Gemini API: {allowed_blocks}")
        if not build:
            print("Using fallback build due to API failure.")
            build, allowed_blocks = generate_default_build(size)
    except Exception as e:
        print(f"Error generating build with Gemini API: {e}")
        print("Using fallback build.")
        build, allowed_blocks = generate_default_build(size)

    # Validate the block structure before proceeding
    if not validate_block_structure(build):
        print("Invalid block structure detected. Using fallback build.")
        build, allowed_blocks = generate_default_build(size)

    # Run the genetic algorithm to improve the build
    print("Starting GA evolution...")
    try:
        # Changed mutation rate to 0.2 and generations to 25
        ga = GeneticAlgorithm(build, build_type, allowed_blocks, population_size=100, mutation_rate=0.2)
        improved_build = ga.evolve(generations=50)
    except Exception as e:
        print(f"Error during GA execution: {e}")
        raise
    print("GA evolution completed.")
    
    # Add doors to the walls after evolution
    print("Adding doors to the walls...")
    try:
        # Determine the center position(s) for the doors
        if size % 2 == 1:  # Odd size
            center = size // 2
            door_width = 1
        else:  # Even size
            center = size // 2 - 1
            door_width = 2

        # Iterate over the second and third layers (layers 1 and 2)
        for layer_idx in [1, 2]:  # Second and third layers
            layer = improved_build[layer_idx]
            
            # North wall (first column)
            for i in range(center, center + door_width):
                layer[i][0] = "AA"  # Replace with air block
                if layer_idx == 1:  # First interior layer
                    layer[i][1] = "AA"  # Clear the block just inside the entrance
                elif layer_idx == 2:  # Second interior layer
                    layer[i][1] = "AA"  # Clear the block just inside the entrance
            
            # South wall (last column)
            for i in range(center, center + door_width):
                layer[i][-1] = "AA"  # Replace with air block
                if layer_idx == 1:  # First interior layer
                    layer[i][-2] = "AA"  # Clear the block just inside the entrance
                elif layer_idx == 2:  # Second interior layer
                    layer[i][-2] = "AA"  # Clear the block just inside the entrance
            
            # East wall (first row)
            for i in range(center, center + door_width):
                layer[0][i] = "AA"  # Replace with air block
                if layer_idx == 1:  # First interior layer
                    layer[1][i] = "AA"  # Clear the block just inside the entrance
                elif layer_idx == 2:  # Second interior layer
                    layer[1][i] = "AA"  # Clear the block just inside the entrance
            
            # West wall (last row)
            for i in range(center, center + door_width):
                layer[-1][i] = "AA"  # Replace with air block
                if layer_idx == 1:  # First interior layer
                    layer[-2][i] = "AA"  # Clear the block just inside the entrance
                elif layer_idx == 2:  # Second interior layer
                    layer[-2][i] = "AA"  # Clear the block just inside the entrance

    except Exception as e:
        print(f"Error adding doors: {e}")
        raise
    
    # Load block abbreviations.
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'block_abbreviations.json')
    with open(data_path, 'r') as f:
        block_abbreviations = json.load(f)
    
    # Create a unique folder for this build.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_description = "".join(c for c in description if c.isalnum() or c in ['-', '_']).lower()
    build_folder = os.path.join(os.path.dirname(__file__), '..', 'output', f"{safe_description}_{size}x{size}_{timestamp}")
    os.makedirs(build_folder, exist_ok=True)
    folder_name = os.path.basename(build_folder)
    print("FOLDER NAME: " + folder_name)
    
    # Save each layer as a text file in the build folder.
    for i, layer in enumerate(improved_build):
        with open(os.path.join(build_folder, f'layer_{i}.txt'), 'w') as f:
            for row in layer:
                print(f"Writing row to file: {row}")  # Debugging line
                # Ensure all items are strings and not lists
                cleaned_row = []
                for block in row:
                    if isinstance(block, list):
                        cleaned_row.append("AA")  # Replace lists with air blocks
                    else:
                        cleaned_row.append(str(block))  # Ensure block is a string
                f.write(' '.join(cleaned_row) + '\n')
        progress_percent = int((i + 1) / len(improved_build) * 100)  # Yield progress
        yield {"type": "progress", "value": progress_percent}

    # Create a schematic file using mcschematic
    schem = mcschematic.MCSchematic()

    # Convert the layers into blocks in the schematic
    for z, layer in enumerate(improved_build):
        for y, row in enumerate(layer):
            for x, block_abbr in enumerate(row):
                if isinstance(block_abbr, list):
                    block_abbr = "AA"  # Replace lists with air blocks
                block_name = block_abbreviations.get(block_abbr, "minecraft:air")  # Default to air if abbreviation is not found
                schem.setBlock((x, z, y), block_name)  # (x, z, y) for Minecraft coordinates

    # Save the schematic file
    schem.save(build_folder, f"{build_type}_{size}x{size}_{timestamp}", mcschematic.Version.JE_1_18_2)

    print(f"Build generated with {size}x{size} size and type {build_type}. Files saved in {build_folder}.")
    yield {"type": "complete", "folder_name": folder_name}
    
def generate_default_build(size):
    # Generate a simple default build
    layers = [
        [["ST" for _ in range(size)] for _ in range(size)],  # Floor
        [["WD" if x == 0 or x == size - 1 or y == 0 or y == size - 1 else "AA" for x in range(size)] for y in range(size)],
        [["WD" if x == 0 or x == size - 1 or y == 0 or y == size - 1 else "AA" for x in range(size)] for y in range(size)],
        [["WD" if x == 0 or x == size - 1 or y == 0 or y == size - 1 else "AA" for x in range(size)] for y in range(size)],# Walls
        [["ST" for _ in range(size)] for _ in range(size)]   # Roof
    ]
    allowed_blocks = ["ST", "WD", "AA"]
    return layers, allowed_blocks