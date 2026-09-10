import random
import math
import struct
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

#Define Crossover helper functions to convert the indiviual floats into 64-bit binary format for crossover and coverting back to float
def float_to_bin64(value:float)->str:
    """Converts any float (positive/negative/fraction) into a 64-bit binary string."""
    # '!d' means network byte order (big-endian) double-precision float
    return ''.join(f'{b:08b}' for b in struct.pack("!d", value))

def bin64_to_float(value:str)->float:
        """Converts a 64-bit binary string back into a signed float."""
        # 1. Split the 64-character string into 8 chunks of 8 bits
        byte_chunks = [value[i:i+8] for i in range(0, 64, 8)]

        # 2. Convert each 8-bit string to an integer, then convert the list to a bytes object
        byte_data = bytes(int(b,2) for b in byte_chunks)

        # 3. Unpack the bytes back into a float (returns a tuple, so we grab index 0)
        return struct.unpack("!d", byte_data)[0]

# Define the crossover function to mix attributes of two parents to create a potentially fitter child

def crossover(parent1: list[float], parent2: list[float]) -> list[float]:
    # convert the bytes into a continous binary string of 64 bits
    binary_parent1 = float_to_bin64(parent1[0])
    binary_parent2 = float_to_bin64(parent2[0])

    # Split the parents at a random point and merge them both to form children
    point = random.randrange(0, len(binary_parent1)-1)
    binary_child1 = binary_parent1[point:] + binary_parent2[:point]
    binary_child2 = binary_parent2[point:] + binary_parent1[:point]

    # Convert the children binary stings to floats and return their values

    c1 = max(-10.0, min(10.0, bin64_to_float(binary_child1)))
    c2 = max(-10.0, min(10.0, bin64_to_float(binary_child2)))
    return [c1, c2]

# Define the mutation function

def mutate(individual: list[float], mutation_rate:float=0.01) ->list[float]:
     binary_individual = list((float_to_bin64(individual[0])))
     binary_individual = [int(i) for i in binary_individual]
     for i in range(len(binary_individual)):
          if random.random() < mutation_rate:
                         binary_individual[i] = 1 - binary_individual[i]
     binary_individual_string = ''.join(map(str, binary_individual))
     return [max(-10.0, min(10.0, bin64_to_float(binary_individual_string)))]

# The main Genetic Algorithm logic incoporating the already defined functions

def genetic_algorithm(generations:int=20):
    population = create_population()
    print(f"Initial Population: {population}")
    for generation in range(generations):
        parents = select(population)
        new_population = []
        while len(new_population) < generations:
               parent1, parent2 = random.sample(parents, 2)
               child1, child2 = crossover(parent1, parent2)
               child1, child2 = mutate([child1]), mutate([child2])
               new_population += child1, child2
        population = new_population
        best_individual = max(population, key=fitness)
        print(f"Generation {generation}: x = {best_individual} fitness = {fitness(best_individual)}")
    return max(population, key=fitness)

genetic_algorithm()