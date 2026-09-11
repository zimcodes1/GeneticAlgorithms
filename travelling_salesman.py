import random
import math

# Define the Cities Class
class City():
    def __init__(self, name, x, y) -> None:
        self.name:str = name
        self.x:int = x
        self.y:int = y
    def to_dict(self):
        return {
            "name":self.name,
            "x":self.x,
            "y":self.y
        }
    def __repr__(self) -> str:
        return f"{self.name}: ({self.x}, {self.y})\n"

# Cities initial dictionary
cities_grid = {
    "London": {"x": 3, "y": 11},
    "Paris": {"x": 5, "y": 7},
    "Brussels": {"x": 6, "y": 10},
    "Luxembourg": {"x": 8, "y": 8},
    "Amsterdam": {"x": 7, "y": 13},
    "Hamburg": {"x": 12, "y": 15},
    "Frankfurt": {"x": 11, "y": 9},
    "Berlin": {"x": 16, "y": 13},
    "Munich": {"x": 14, "y": 6},
    "Zurich": {"x": 11, "y": 4}
}
# Convert the cities dictionary to instances of the City class

A, B, C, D, E, F, G, H, I, J = [City(name=x, x=cities_grid[x].get("x"), y=cities_grid[x].get('y')) for x in cities_grid.keys()]
cities_list = [A, B, C, D, E, F, G, H, I, J]

# Define function to create an individual candidate solution

def create_individual() -> list[City]:
    return random.sample(cities_list, 10)

# Define function to create initial polulation of random possible solutions

def create_population(size:int = 10) ->list[list[City]]:
    return [create_individual() for _ in range(size)]

# Distance calculators helper functions

def distance(city1:City, city2:City) -> float:
    """
    This is an implementation of the Euclidean distance formula i.e
    `d = sqrt((x2 - x1)^2 + (y2 - y1)^2)`

    This function calculates the total distances between 2 cities
    """
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2)

# Total distance
def route_distance(route: list[City]) -> float:
    """This calculates the total distances between all cities provided in a route"""
    total_distance:float = 0.0
    for path in range(len(route)):
        city1 = route[path]
        city2 = route[(path + 1) % len(route)]
        total_distance += distance(city1, city2)
    return total_distance

# Fitness function for evaluating how good a route is

def route_fitness(route: list[City]) -> float:
    """
    This takes in a route i.e a list of `City` objects, 
    calcuates the total distance between them using the `route_distance()` 
    function and inverts it to return the fitness value. 
    

    **Note:** longer distance = lower fitness and vice versa
    """

    return 1/route_distance(route)

# Selection function for selecting the fittest individuals for crossover

def select_fittest_route(route: list[list[City]]) -> list[list[City]]:
    """Takes in a population of routes and returns the 6 fittest routes for crossover"""
    route.sort(key=route_fitness, reverse=True)
    return route[:6]

# Crossover function: Ordered Crossover (OX)

def crossover(parent1:list[City], parent2:list[City]) -> list[list[City | None]]:
    # Take a section from a parent and replace it with another from the other parent
    start = random.randrange(0, int(len(parent1)/2))

    def create_child(p1:list[City], p2:list[City]):
        #Initialize an empty child array
        child : list[City | None] = [None] * len(p1)
        #Copy the slice from the first parent
        child[start:start+4] = p1[start:start+4]
        # Fill the remaining spots with cities using order from the second parent
        # We start filling right after the copied segment
        current_pos = (start+4) % len(p1)
        for city in p2:
            if city not in child:
                child[current_pos] = city
                current_pos = (current_pos + 1) % len(p1)
        return child
    return [create_child(parent1, parent2), create_child(parent2, parent1)]

# Mutation function: Swap Mutation
def mutate(route: list[City|None], mutation_rate:float=0.01) -> list[City | None]:
    """Swap two cities within the same route, introduces no duplicates"""
    if random.random() < mutation_rate:
        points = random.sample(range(len(route)), 2)
        route[points[0]], route[points[1]] = route[points[1]], route[points[0]]
    return route

#The main genetic algorithm function
def genetic_algorithm(generations:int = 100, population_size:int = 50, mutation_rate:float = 0.02):
    population = create_population(population_size)
    print(f"\nInitial generation: {population}\n")

    for generation in range(generations):
        new_population = []

        # Preserve the best route
        best_individual = min(population, key=route_distance)
        new_population.append(best_individual.copy())

        parents = select_fittest_route(population)

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            child1, child2 = mutate(child1, mutation_rate=mutation_rate), mutate(child2, mutation_rate=mutation_rate)
            new_population += child1, child2

        population = new_population
        population.sort(key=route_fitness, reverse=True)

        print(f"Generation {generation + 1}: \nShortest route: {population[0]}, Route Distance: {route_distance(population[0])}")
    print(f"Final Result: {population[0]}, Distance: {route_distance(population[0])}")
    return population[0]
    
genetic_algorithm()