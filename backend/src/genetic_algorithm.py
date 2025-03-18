import random
import json
import os
from heuristics import evaluate_fitness

# Load block abbreviations
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'block_abbreviations.json')
with open(data_path, 'r') as f:
    block_abbreviations = json.load(f)

class GeneticAlgorithm:
    def __init__(self, initial_build, build_type, allowed_blocks, population_size=100, mutation_rate=0.1):
        self.initial_build = initial_build
        self.build_type = build_type
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.first_interior_layer_meets_ratio = False  # Flag to track if the first interior layer meets the ratio
        self.allowed_blocks = set(allowed_blocks)  # Use the allowed blocks from Gemini
        self.population = self.initialize_population()
        
    def get_allowed_blocks(self, build_type):
        # Define the mapping of keywords to allowed blocks
        return self.allowed_blocks

    def initialize_population(self):
        # Create an initial population based on the initial build
        population = []
        for _ in range(self.population_size):
            # Create variations of the initial build
            mutated_build = self.mutate_build(self.initial_build)
            # Add some useful blocks to the first interior layer
            for row_idx, row in enumerate(mutated_build[1]):  # First interior layer
                for block_idx in range(len(row)):
                    if self.is_interior_block(1, row_idx, block_idx, mutated_build):  # Check if it's an interior block
                        if random.random() < 0.1:  # 10% chance to add a useful block
                            row[block_idx] = random.choice(self.get_random_useful_block())
            population.append(mutated_build)
        return population

    # Changed random further reduction to .02 to encourage more mutation
    # Changed useful block % to 30
    def mutate_build(self, build):
        # Apply random mutations to the build
        mutated_build = []

        # Count the number of each useful block in the build
        useful_blocks_count = {block: 0 for block in self.get_random_useful_block()}
        for layer in build:
            for row in layer:
                for block in row:
                    if isinstance(block, list):
                        continue  # Skip if block is a list
                    if block in useful_blocks_count:
                        useful_blocks_count[block] += 1

        # Calculate the total number of useful blocks
        total_useful_blocks = sum(useful_blocks_count.values())

        for layer_idx, layer in enumerate(build):
            mutated_layer = []
            for row_idx, row in enumerate(layer):
                mutated_row = []
                for block_idx, block in enumerate(row):
                    # Skip mutation for border blocks in the first interior layer
                    if self.is_first_interior_layer(layer_idx, build) and not self.is_interior_block(layer_idx, row_idx, block_idx, build):
                        mutated_row.append(block)  # Preserve border blocks
                        continue

                    if random.random() <= self.mutation_rate:
                        # Only mutate the first interior layer if it hasn't met the ratio
                        if self.is_first_interior_layer(layer_idx, build) and self.is_interior_block(layer_idx, row_idx, block_idx, build):
                            # Calculate the current ratio of useful blocks
                            first_interior_layer = build[1]
                            total_blocks = len(first_interior_layer) * len(first_interior_layer[0])
                            useful_blocks = sum(row.count(block) for row in first_interior_layer for block in self.get_random_useful_block())
                            useful_percentage = (useful_blocks / total_blocks) * 100

                            # Only add a useful block if the current percentage is below the desired threshold
                            if useful_percentage < 20:  # Adjust this threshold as needed
                                if random.random() < 0.02:  # Further reduce the chance of adding a useful block
                                    # Select a useful block proportionally based on current counts
                                    if total_useful_blocks > 0:
                                        # Calculate the probability of selecting each block
                                        block_probabilities = {
                                            block: (1 - (count / total_useful_blocks)) for block, count in useful_blocks_count.items()
                                        }
                                        # Normalize probabilities
                                        total_probability = sum(block_probabilities.values())
                                        if total_probability > 0:
                                            block_probabilities = {block: prob / total_probability for block, prob in block_probabilities.items()}
                                            # Select a block based on the probabilities
                                            selected_block = random.choices(list(block_probabilities.keys()), weights=block_probabilities.values())[0]
                                            mutated_row.append(selected_block)
                                        else:
                                            # If all blocks are equally distributed, select randomly
                                            mutated_row.append(self.get_random_useful_block())
                                    else:
                                        # If no useful blocks are present, select randomly
                                        mutated_row.append(self.get_random_useful_block())
                                else:
                                    mutated_row.append("AA")  # Replace with air block
                            else:
                                mutated_row.append(block)  # Preserve the block
                        else:
                            mutated_row.append(block)  # Preserve walls, roof, and other layers
                    else:
                        mutated_row.append(block)
                mutated_layer.append(mutated_row)
            mutated_build.append(mutated_layer)
        return mutated_build

    def is_interior_block(self, layer_idx, row_idx, block_idx, build):
        # Check if the block is part of the interior (not walls or roof)
        # Assuming the first and last layers are floor and roof, and the outer rows/columns are walls
        if layer_idx == 0 or layer_idx == len(build) - 1:
            return False  # Floor and roof layers are not interior
        if row_idx == 0 or row_idx == len(build[layer_idx]) - 1:
            return False  # Outer rows are walls
        if block_idx == 0 or block_idx == len(build[layer_idx][row_idx]) - 1:
            return False  # Outer columns are walls
        return True  # Interior block

    def get_random_allowed_block(self):
        # Return a random block from the allowed blocks
        return random.choice(list(self.allowed_blocks))

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create a child
        child = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def evolve(self, generations=25):
        for generation in range(generations):
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child = self.crossover(parent1, parent2)
                child = self.mutate_build(child)
                new_population.append(child)
            self.population = new_population

            # Log fitness scores
            fitness_scores = [evaluate_fitness(build, self.allowed_blocks) for build in self.population]
            average_fitness = sum(fitness_scores) / len(fitness_scores)
            best_fitness = max(fitness_scores)
            print(f"Generation {generation + 1}: Average Fitness = {average_fitness}, Best Fitness = {best_fitness}")

            # Check if the first interior layer meets the desired ratio
            self.first_interior_layer_meets_ratio = self.check_first_interior_layer_ratio()

        # Return the best build after evolution
        return self.get_best_build()

    def select_parent(self):
        # Select a parent based on fitness (roulette wheel selection)
        fitness_scores = [evaluate_fitness(build, self.allowed_blocks) for build in self.population]
        total_fitness = sum(fitness_scores)
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, build in enumerate(self.population):
            current += fitness_scores[i]
            if current > pick:
                return build
        return self.population[0]

    def get_best_build(self):
        # Return the build with the highest fitness score
        fitness_scores = [evaluate_fitness(build, self.allowed_blocks) for build in self.population]
        best_index = fitness_scores.index(max(fitness_scores))
        return self.population[best_index]

    def is_first_interior_layer(self, layer_idx, build):
        # Check if the layer is the first interior layer (layer 1)
        return layer_idx == 1  # First interior layer is layer 1 (layer 0 is the floor)

    def get_random_useful_block(self):
    # Return a list of all useful blocks
        return ["CT", "FN", "BF", "SM", "CBF", "LBF", "SFB", "STB", "BFB"]

    def check_first_interior_layer_ratio(self):
        # Check if the first interior layer meets the desired ratio (80% air, 20% useful blocks) with 5% leeway
        for build in self.population:
            first_interior_layer = build[1]  # First interior layer is layer 1
            total_blocks = len(first_interior_layer) * len(first_interior_layer[0])
            air_blocks = sum(row.count("AA") for row in first_interior_layer)
            useful_blocks = sum(row.count(block) for row in first_interior_layer for block in self.get_random_useful_block())

            air_percentage = (air_blocks / total_blocks) * 100
            useful_percentage = (useful_blocks / total_blocks) * 100

            # Check if the ratio is within 5% leeway
            if 80 <= air_percentage <= 90 and 10 <= useful_percentage <= 20:
                return True  # Ratio is met
        return False  # Ratio is not met
