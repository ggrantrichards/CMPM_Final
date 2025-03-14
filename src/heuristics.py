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
    if len(wall1) != len(wall2):
        return 0  # Walls must be the same length

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
    # Implement the logic here
    return score

def thematic_consistency(build):
    # Define the mapping of keywords to allowed and disallowed blocks
    thematic_keywords = {
        "house": {
            "allowed": {"WD", "SP", "BP", "JP", "AP", "DP", "CP", "WP", "OL", "SL", "BL", "DL", "OS", "SS", "BS", "JS", "AS", "DOS"},
            "disallowed": {"NT", "OB", "BB", "PBS", "PBSB"}
        },
        "castle": {
            "allowed": {"ST", "CB", "SB", "BR", "NT", "EB"},
            "disallowed": {"WD", "SP", "BP", "JP", "AP", "DP", "CP", "WP"}
        },
        "nether": {
            "allowed": {"NT", "BB", "PBS", "PBSB", "CLG", "CS"},
            "disallowed": {"WD", "SP", "BP", "JP", "AP", "DP", "CP", "WP"}
        },
        "modern": {
            "allowed": {"GL", "ST", "PDI", "PAN", "PDS", "PBS"},
            "disallowed": {"WD", "SP", "BP", "JP", "AP", "DP", "CP", "WP", "NT"}
        }
    }

    # Determine the build type from the description
    build_type = "house"  # Default to house if no keyword matches
    for keyword in thematic_keywords:
        if keyword in build_type:
            build_type = keyword
            break

    allowed_blocks = thematic_keywords[build_type]["allowed"]
    disallowed_blocks = thematic_keywords[build_type]["disallowed"]

    # Calculate the thematic consistency score
    score = 0
    total_blocks = 0
    for layer in build:
        for row in layer:
            for block in row:
                total_blocks += 1
                if block in allowed_blocks:
                    score += 1
                elif block in disallowed_blocks:
                    score -= 1

    return score / total_blocks  # Normalize the score

def interior_validation(build):
    # Check if the interior is mostly hollow
    # Return a score based on the interior quality 
    # First interior layer: 80% air blocks, 20% useful blocks
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

    # Calculate deviation from 80% air and 20% useful blocks
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