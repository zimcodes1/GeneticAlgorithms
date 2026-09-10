import random
import math
"""

This genetic algorithm finds the value of x that maximises the function: f(x) = x^2 + 10sin(x)

"""

# Define function for creating individuals

def create_individual() -> list[float]:
    return [random.uniform(-10.0, 10.0)]

# Define fitness function for evaluating the fitness each individual's value

def fitness(individual: list[float]) -> float:
    return individual[0]**2 + 10*math.sin(individual[0])

# Define the funtion for creating the initial population

def create_population(size:int=10)->list[list[float]]:
    population = []
    for _ in range(size):
        population.append(create_individual())
    return population

# Define the selection function to select the fittest values of x for crossover

def select(population: list[list[float]])->list[list[float]]:
    population.sort(key=fitness, reverse=True)
    return population[:6]

# Define the crossover function using blend crossover (BLX-alpha)

def crossover(parent1: list[float], parent2: list[float]) -> list[float]:
    alpha = 0.5
    lo, hi = min(parent1[0], parent2[0]), max(parent1[0], parent2[0])
    spread = (hi - lo) * alpha
    c1 = random.uniform(max(-10.0, lo - spread), min(10.0, hi + spread))
    c2 = random.uniform(max(-10.0, lo - spread), min(10.0, hi + spread))
    return [c1, c2]

# Define the mutation function

def mutate(individual: list[float], mutation_rate: float=0.01) -> list[float]:
    x = individual[0]
    if random.random() < mutation_rate:
        x = max(-10.0, min(10.0, x + random.gauss(0, 1)))
    return [x]

# The main Genetic Algorithm logic incoporating the already defined functions

def genetic_algorithm(generations:int=20):
    population = create_population()
    print(f"Initial Population: {population}")
    for generation in range(generations):
        parents = select(population)
        new_population = []
        while len(new_population) < 10:
               parent1, parent2 = random.sample(parents, 2)
               child1, child2 = crossover(parent1, parent2)
               child1, child2 = mutate([child1]), mutate([child2])
               new_population += child1, child2
        population = new_population
        best_individual = max(population, key=fitness)
        print(f"Generation {generation +1}: x = {best_individual} fitness = {fitness(best_individual)}")
    return max(population, key=fitness)

genetic_algorithm()