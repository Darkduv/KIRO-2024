from typing import Any
from KIRO.export import to_json

class Template : 
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

class Template2 : 
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

# to_json(
#     {1:1, 2:'a', 3:Template(1,2,3), 4:[Template(1,2,3), Template2(1,2,3)]}
# )

import random

from KIRO.algorithms import GeneticAlgorithm


population_size = 500
gene_length = 10
compute_generations = 1000
mutation_rate = 0.05

initial_population = [
    [random.random() for _ in range(gene_length)]
    for _ in range(population_size)
]

class GeneticTest(GeneticAlgorithm):
    def fitness(self, individual: Any) -> float:
        return -sum([elem**2 for elem in individual])
    
    def crossover(self, indiv1: Any, indiv2: Any) -> Any:
        return indiv1[:gene_length//2]+indiv2[gene_length//2:]
    
    def mutate(self, indiv1: Any) -> Any:
        return [elem+(random.random()-0.5)*mutation_rate for elem in indiv1]

ALGO = GeneticTest(
    initial_population=initial_population,
    number_of_best_indiv=population_size//10,
)

ALGO.compute_generations(compute_generations)

print(ALGO.last_generation)