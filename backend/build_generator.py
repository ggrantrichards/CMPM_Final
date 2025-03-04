import json
import os
from gemini_api import generate_build_with_gemini

def generate_build(size, build_type):
    layers = generate_build_with_gemini(size, build_type)

    # Load block abbreviations
    with open('data/block_abbreviations.json', 'r') as f:
        block_abbreviations = json.load(f)

    # Save each layer as a text file
    for i, layer in enumerate(layers):
        with open(f'output/layer_{i}.txt', 'w') as f:
            for row in layer:
                f.write(' '.join(row) + '\n')

    print(f"Build generated with {size}x{size} size and type {build_type}.")