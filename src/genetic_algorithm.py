import random
import json
import os
from heuristics import evaluate_fitness

# Load block abbreviations
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'block_abbreviations.json')
with open(data_path, 'r') as f:
    block_abbreviations = json.load(f)

class GeneticAlgorithm:
    def __init__(self, initial_build, population_size=10, mutation_rate=0.1):
        self.initial_build = initial_build
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        # Create an initial population based on the initial build
        population = []
        for _ in range(self.population_size):
            # Create variations of the initial build
            population.append(self.mutate_build(self.initial_build))
        return population

    def mutate_build(self, build):
        # Apply random mutations to the build
        mutated_build = []
        for layer in build:
            mutated_layer = []
            for row in layer:
                mutated_row = []
                for block in row:
                    if random.random() < self.mutation_rate:
                        # Mutate the block (e.g., change it to a random block)
                        mutated_row.append(self.get_random_block())
                    else:
                        mutated_row.append(block)
                mutated_layer.append(mutated_row)
            mutated_build.append(mutated_layer)
        return mutated_build

    def get_random_block(self):
        # Return a random block from the block abbreviations
        blocks = list(block_abbreviations.keys())
        return random.choice(blocks)

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create a child
        child = []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def evolve(self, generations=10):
        for _ in range(generations):
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child = self.crossover(parent1, parent2)
                child = self.mutate_build(child)
                new_population.append(child)
            self.population = new_population

        # Return the best build after evolution
        return self.get_best_build()

    def select_parent(self):
        # Select a parent based on fitness (roulette wheel selection)
        fitness_scores = [evaluate_fitness(build) for build in self.population]
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
        fitness_scores = [evaluate_fitness(build) for build in self.population]
        best_index = fitness_scores.index(max(fitness_scores))
        return self.population[best_index]