def evaluate_fitness(build, allowed_blocks):
    fitness = 0
    fitness += four_wall_validation(build) * 0.2  # 20% weight
    fitness += roofline_validation(build) * 0.2    # 20% weight
    fitness += thematic_consistency(build, allowed_blocks) * 0.2   # 20% weight
    fitness += interior_validation(build) * 0.4    # 40% weight
    return fitness

def four_wall_validation(build):
    # Check if the build has four walls that are similar but not necessarily symmetrical
    # Return a score based on how many walls the build seems to have
    # Make sure not too many large gaps
    score = 0

    # if not build:
    #     return score

    # size = len(build[0])
    # walls = {"north": [], "south": [], "east": [], "west": []}

    # # Extract the walls from all layers
    # for layer in build:
    #     north_wall = [row[0] for row in layer]  # First column
    #     south_wall = [row[-1] for row in layer]  # Last column
    #     east_wall = layer[0]  # First row
    #     west_wall = layer[-1]  # Last row

    #     walls["north"].append(north_wall)
    #     walls["south"].append(south_wall)
    #     walls["east"].append(east_wall)
    #     walls["west"].append(west_wall)

    # # Compare each wall to the others and calculate similarity
    # wall_keys = list(walls.keys())
    # for i in range(len(wall_keys)):
    #     for j in range(i + 1, len(wall_keys)):
    #         similarity = calculate_similarity(walls[wall_keys[i]], walls[wall_keys[j]])
    #         if similarity >= 0.9:  # 90% similarity
    #             score += 25  # Add to the score if walls are similar
    #         else:
    #             score -= 25  # Penalize if walls are not similar

    return score

def calculate_similarity(wall1, wall2):
    # Calculate the similarity between two walls based on block composition
    # if len(wall1) != len(wall2):
    #     return 0  # Do walls really need to be of the same length?

    similar_blocks = 0
    total_blocks = 0
    for layer1, layer2 in zip(wall1, wall2):
        for block1, block2 in zip(layer1, layer2):
            total_blocks += 1
            if block1 == block2:
                similar_blocks += 1

    return similar_blocks / total_blocks

def roofline_validation(build):
    # Check if the build has a defined roofline
    # Return a score based on The structure of the roof
    # Preferred to have a sloped or tapered design
    score = 0
    if not build:
        return score
    roof = build[-1] # Assuming the roof is the last complete layer that we have at the moment. This should just be a solid flat block above the walls.
                    # Think of it as the base of the roof.

    base_size = len(build[0])
    roof_size = len(build[-1])

    if base_size != roof_size:
        return score - 25

    for block in roof:
        if block == "AA":
            score -= 25
        else:
            continue
    return score

def thematic_consistency(build, allowed_blocks):
    # Define the mapping of keywords to allowed and disallowed blocks
    score = 0
    total_blocks = 0

    for layer in build:
        for row in layer:
            for block in row:
                total_blocks += 1
                if block in allowed_blocks:
                    score += 1  # Reward for using allowed blocks
                else:
                    score -= 1  # Penalize for using disallowed blocks

    # Normalize the score by dividing by the total number of blocks
    if total_blocks == 0:
        return 0  # Avoid division by zero
    return score / total_blocks


def interior_validation(build):
    # Check if the interior is mostly hollow
    # Return a score based on the interior quality
    # First interior layer: 90% air blocks, 10% useful blocks
    # Remaining interior layers: 95% air blocks, 5% other blocks
    fitness = 0
    useful_blocks = {"CT", "FN", "BF", "SM", "CBF", "LBF", "SFB", "STB", "BFB"}
    interior_layers = build[1:-1]  # Skip the first layer (floor) and the last layer (roof)

    if not interior_layers:
        return -100  # Penalize heavily for invalid builds

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
    fitness -= (air_deviation_first_layer + useful_deviation_first_layer)  # Subtract deviation from fitness

    # Remaining interior layers (no mutations allowed, so no validation needed)
    # We can optionally enforce 95% air blocks, but mutations are not allowed here
    for layer in interior_layers[1:]:
        total_blocks_layer = len(layer) * len(layer[0])
        air_blocks_layer = sum(row.count("AA") for row in layer)
        air_percentage_layer = (air_blocks_layer / total_blocks_layer) * 100

        # Calculate deviation from 95% air blocks
        air_deviation_layer = abs(air_percentage_layer - 80)
        fitness -= air_deviation_layer  # Subtract deviation from fitness

    return fitness