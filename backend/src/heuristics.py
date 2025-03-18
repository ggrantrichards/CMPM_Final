def evaluate_fitness(build, allowed_blocks):
    fitness = 0
    fitness += roofline_validation(build) * .2
    fitness += thematic_consistency(build, allowed_blocks) * .4 # I think these two are equally important for an aesthetic build
    fitness += interior_validation(build) * .4
    return fitness

# Removed 4 wall validation & calculate similarity
# def four_wall_validation(build):
#     # Check if the build has four walls that are similar but not necessarily symmetrical
#     # Return a score based on how many walls the build seems to have
#     # Make sure not too many large gaps
#     score = 0
#     return score
#
# def calculate_similarity(wall1, wall2):
#     # Calculate the similarity between two walls based on block composition
#     similar_blocks = 0
#     total_blocks = 0
#     for layer1, layer2 in zip(wall1, wall2):
#         for block1, block2 in zip(layer1, layer2):
#             total_blocks += 1
#             if block1 == block2:
#                 similar_blocks += 1
#
#     return similar_blocks / total_blocks

def roofline_validation(build):
    # Check if the build has a defined roofline
    # Return a score based on The structure of the roof
    # Preferred to have a sloped or tapered design
    score = 0
    if not build:
        score -= 1
        return score
    roof = build[-1] # Assuming the roof is the last complete layer that we have at the moment. This should just be a solid flat block above the walls.
                    # Think of it as the base of the roof.

    base_size = len(build[0])
    roof_size = len(build[-1])

    if base_size != roof_size:
        score -= 0.5
    else:
        score += 0.5

    for block in roof:
        if block == "AA":
            score -= 0.2
        else:
            score += 0.2
    return score

def thematic_consistency(build, allowed_blocks):
    # Ensure allowed_blocks is a set
    allowed_blocks = set(allowed_blocks)
    
    score = 0
    total_blocks = 0

    for layer in build:
        for row in layer:
            for block in row:
                # print(f"Block type: {type(block)}, Block value: {block}")  # Debugging line
                if isinstance(block, list):
                    # print(f"Skipping block because it is a list: {block}")
                    continue  # Skip if block is a list
                total_blocks += 1
                if block in allowed_blocks:
                    score += 0.75  # Reward for using allowed blocks
                else:
                    score -= 0.75 # Penalize for using disallowed blocks

    # Normalize the score by dividing by the total number of blocks
    if total_blocks == 0:
        return 0  # Avoid division by zero
    fitness = score/total_blocks
    return fitness

def interior_validation(build):
    # Check if the interior is mostly hollow
    # Return a score based on the interior quality
    # First interior layer: 90% air blocks, 10% useful blocks
    # Remaining interior layers: 95% air blocks, 5% other blocks
    # Can't use 0 otherwise it'll always be a negative fitness.

    useful_blocks = {"CT", "FN", "BF", "SM", "CBF", "LBF", "SFB", "STB", "BFB"}
    interior_layers = build[1:-1]  # Skip the first layer (floor) and the last layer (roof)

    if not interior_layers:
        return -1  # Penalize heavily for invalid builds, this is basically -100% fitness.

    # First interior layer
    first_interior_layer = interior_layers[0]
    total_blocks_first_layer = len(first_interior_layer) * len(first_interior_layer[0])
    air_blocks_first_layer = sum(row.count("AA") for row in first_interior_layer)
    useful_blocks_first_layer = sum(row.count(block) for row in first_interior_layer for block in useful_blocks)

    air_percentage_first_layer = (air_blocks_first_layer / total_blocks_first_layer) * 100
    useful_percentage_first_layer = (useful_blocks_first_layer / total_blocks_first_layer) * 100

    # Calculate deviation from 90% air and 10% useful blocks
    air_deviation_first_layer = abs(air_percentage_first_layer - 80)
    useful_deviation_first_layer = abs(useful_percentage_first_layer - 20)
    total_deviation = (air_deviation_first_layer/100 + useful_deviation_first_layer/100)  # Subtract deviation from fitness

    if total_deviation <= .15:
        fitness = 1
    elif total_deviation > .15 and total_deviation <= .25:
        fitness = 0.7
    elif total_deviation > .25 and total_deviation <= .4:
        fitness = 0.5
    elif total_deviation > .4 and total_deviation <= 0.5:
        fitness = 0.35
    else:
        fitness = 0.2

    # Remaining interior layers (no mutations allowed, so no validation needed)
    # We can optionally enforce 95% air blocks, but mutations are not allowed here
    for layer in interior_layers[1:]:
        total_blocks_layer = len(layer) * len(layer[0])
        air_blocks_layer = sum(row.count("AA") for row in layer)
        air_percentage_layer = (air_blocks_layer / total_blocks_layer) * 100

        # Calculate deviation from 95% air blocks
        air_deviation_layer = abs(air_percentage_layer - 80)
        fitness -= air_deviation_layer/100  # Subtract deviation from fitness
    return fitness