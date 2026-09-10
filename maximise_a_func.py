import random

"""

This genetic algorithm finds the value of x between 0 and 31 that maximises the function: f(x) = x^2

"""

# Define function for creating individuals

def create_individual() -> list[int]:
    """This returns a 5-items list of randomly generated binary digits"""
    return [random.randint(0, 1) for _ in range(5)]

# Define function that converts the chromosomes into a number

def decode(individual:list[int]) -> int:
    """Converts the randomly generated individuals into their decimal values"""
    return int("".join(map(str, individual)), 2)

# Define fitness function

def fitness(individual: list[int]) ->int:
    """Returns the fitness of an individual"""
    x = decode(individual)
    return x**2

# Define a function to create a population of individuals

def create_population(size:int) -> list[list[int]]:
    """Generates and returns a population of individuals given a **`population size`**"""
    return [create_individual() for _ in range(size)]

# Define the selection function to select the fittest individuals: Elitism Selection

def select_fittest(population: list[list[int]]) -> list[list[int]]:
    """Selects the 4 fittest individuals from a population for the next phase"""
    population.sort(key=fitness, reverse=True)
    return population[:4]

# Define crossover function for generating children from fit individuals

def crossover(parent1:list[int], parent2:list[int]) -> list[list[int]]:
    """Takes two parent individuals and creates two children from both by spliting and merging them at a random point"""
    point = random.randint(1, len(parent1) -1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return [child1, child2]

# Define mutation function to randomly flip a binary digit in an individual to introduce diversity in a population

def mutate(individual: list[int], mutation_rate:float = 0.01) ->list[int]:
    """Takes in an individual and randomly flips a bit at a defined rate `mutation_rate`: **default=0.01 i.e 1%**"""
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]

    return individual

def genetic_algorithm():
    population = create_population(10)
    print(population)
    for generation in range(20):

        # Select the fittest individuals from the original population
        parents = select_fittest(population)

        # Create a new population
        new_population = []

        while len(new_population) < 20:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            child1, child2 = mutate(child1, mutation_rate=0.1), mutate(child2, mutation_rate=0.1)

            #Add children to the new population
            new_population += child1, child2
        population = new_population

        # Find the best individual after iterating 20 times
        best_individual =  max(population, key=fitness)

        print(f"Generation {generation}: x = {best_individual} fitness = {fitness(best_individual)}")
    return max(population, key=fitness)

best = genetic_algorithm()

print(
    f"\nBest Solution: x = {decode(best)} fitness = {fitness(best)}"
)