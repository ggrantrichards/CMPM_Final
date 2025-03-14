def evaluate_fitness(build):
    fitness = 0
    fitness += four_wall_validation(build)
    fitness += roofline_validation(build)
    fitness += thematic_consistency(build)
    fitness += interior_validation(build)
    return fitness

def four_wall_validation(build):
    # Check if the build has four walls that are similar but not necessarily symmetrical
    # Return a score based on how many walls the build seems to have 
    # Make sure not too many large gaps
    score = 0
    # Implement the logic here
    return score

def roofline_validation(build):
    # Check if the build has a defined roofline
    # Return a score based on The structure of the roof 
    # Preferred to have a sloped or tapered design
    score = 0
    # Implement the logic here
    return score

def thematic_consistency(build):
    # Check if the build is thematically consistent
    # Return a score based on thematic consistency 
    # Use the appropriate blocks with the correct indication of key words in the build description
    score = 0
    # Implement the logic here
    return score

def interior_validation(build):
    # Check if the interior is mostly hollow
    # Return a score based on the interior quality 
    # First interior layer: 80% air blocks, 20% useful blocks
    # Remaining interior layers: 95% air blocks, 5% other blocks
    score = 0

    # List of useful blocks
    useful_blocks = {"CT", "FN", "BF", "SM", "CBF", "LBF", "SFB", "STB", "BFB"}

    # Skip the first layer (floor) and the last layer (roof)
    interior_layers = build[1:-1]

    # Check the first interior layer (layer 1, after the floor)
    first_interior_layer = interior_layers[0]

    # Count the total number of blocks in the first interior layer
    total_blocks_first_layer = len(first_interior_layer) * len(first_interior_layer[0])

    # Count the number of air blocks and useful blocks in the first interior layer
    air_blocks_first_layer = 0
    useful_blocks_first_layer = 0

    for row in first_interior_layer:
        for block in row:
            if block == "AA":  # Air block
                air_blocks_first_layer += 1
            elif block in useful_blocks:  # Useful block
                useful_blocks_first_layer += 1

    # Calculate the percentage of air and useful blocks in the first interior layer
    air_percentage_first_layer = (air_blocks_first_layer / total_blocks_first_layer) * 100
    useful_percentage_first_layer = (useful_blocks_first_layer / total_blocks_first_layer) * 100

    # Check if the first interior layer meets the requirements
    if air_percentage_first_layer >= 80 and useful_percentage_first_layer <= 20:
        score += 50  # Add to the score if the first interior layer meets the requirements

    # Check the remaining interior layers (layers 2 and above)
    for layer in interior_layers[1:]:
        # Count the total number of blocks in the current layer
        total_blocks_layer = len(layer) * len(layer[0])

        # Count the number of air blocks in the current layer
        air_blocks_layer = 0
        for row in layer:
            for block in row:
                if block == "AA":  # Air block
                    air_blocks_layer += 1

        # Calculate the percentage of air blocks in the current layer
        air_percentage_layer = (air_blocks_layer / total_blocks_layer) * 100

        # Check if the current layer meets the 95% air block requirement
        if air_percentage_layer >= 95:
            score += 10  # Add to the score if the layer meets the requirement
        else:
            score -= 10  # Penalize the score if the layer does not meet the requirement

    return score

# entrance validation should be done before GA
# def entrance_validation(build):
#     # Check if there is one open entrance 1x1x2 in the center of a wall
#     # Return a score based on the entrance quality
#     # Make sure there is only one entrance and it is in the center of a wall 
#     # If even build size then prefer 2x1x2 entrance
#     score = 0
#     # Implement the logic here
#     return score