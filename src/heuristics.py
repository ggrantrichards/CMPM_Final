def evaluate_fitness(build):
    fitness = 0
    fitness += four_wall_validation(build) * 0.2  # 20% weight
    fitness += roofline_validation(build) * 0.2    # 20% weight
    fitness += thematic_consistency(build) * 0.2   # 20% weight
    fitness += interior_validation(build) * 0.4    # 40% weight
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
    fitness = 0
    useful_blocks = {"CT", "FN", "BF", "SM", "CBF", "LBF", "SFB", "STB", "BFB"}
    interior_layers = build[1:-1]

    if not interior_layers:
        return -100  # Penalize heavily for invalid builds

    # First interior layer
    first_interior_layer = interior_layers[0]
    total_blocks_first_layer = len(first_interior_layer) * len(first_interior_layer[0])
    air_blocks_first_layer = sum(row.count("AA") for row in first_interior_layer)
    useful_blocks_first_layer = sum(row.count(block) for row in first_interior_layer for block in useful_blocks)

    air_percentage_first_layer = (air_blocks_first_layer / total_blocks_first_layer) * 100
    useful_percentage_first_layer = (useful_blocks_first_layer / total_blocks_first_layer) * 100

    # Calculate deviation from 80% air and 20% useful blocks
    air_deviation_first_layer = abs(air_percentage_first_layer - 80)
    useful_deviation_first_layer = abs(useful_percentage_first_layer - 20)
    fitness -= (air_deviation_first_layer + useful_deviation_first_layer)  # Subtract deviation from fitness

    # Remaining interior layers
    for layer in interior_layers[1:]:
        total_blocks_layer = len(layer) * len(layer[0])
        air_blocks_layer = sum(row.count("AA") for row in layer)
        air_percentage_layer = (air_blocks_layer / total_blocks_layer) * 100

        # Calculate deviation from 95% air blocks
        air_deviation_layer = abs(air_percentage_layer - 95)
        fitness -= air_deviation_layer  # Subtract deviation from fitness

    return fitness

# entrance validation should be done before GA
# def entrance_validation(build):
#     # Check if there is one open entrance 1x1x2 in the center of a wall
#     # Return a score based on the entrance quality
#     # Make sure there is only one entrance and it is in the center of a wall 
#     # If even build size then prefer 2x1x2 entrance
#     score = 0
#     # Implement the logic here
#     return score