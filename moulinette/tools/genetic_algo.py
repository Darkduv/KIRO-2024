import random

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Optional, Type, List

__all__ = ["ChromosomeABC", "PopulationABC", "GeneticAlgo",
           "Chrom", "GenericPop"]


Chrom = TypeVar('Chrom', bound="ChromosomeABC")
GenericPop = TypeVar('GenericPop', bound="PopulationABC")


class ChromosomeABC(ABC):
    @abstractmethod
    def mutate(self: Chrom) -> Chrom:
        ...

    @classmethod
    @abstractmethod
    def crossover(cls: Type[Chrom], parent1: Chrom, parent2: Chrom)\
            -> Chrom:
        ...

    @classmethod
    def make_mutated_child(cls: Type[Chrom], parent1: Chrom,
                           parent2: Chrom) \
            -> Chrom:
        child = parent1.crossover(parent1, parent2)
        return child.mutate()

    @property
    @abstractmethod
    def score(self) -> float:
        ...

    def __lt__(self: Chrom, other: Chrom):
        return self.score < other.score


class PopulationABC(ABC, Generic[Chrom]):

    def __init__(self, population: List[Chrom]):
        self.population = population

    @property
    def len_pop(self) -> int:
        return len(self.population)

    @abstractmethod
    def selection(self) -> List[Chrom]:
        """Select two part of the population.

        First is the "good" one, second is the "bad" one"""
        ...

    def __iter__(self):
        return self.population.__iter__()

    def new_generation(self: GenericPop) -> GenericPop:
        selected = self.selection()
        nb_children = self.len_pop - len(selected)
        children = []
        for _ in range(nb_children):
            parent1, parent2 = random.sample(self.population, k=2)
            child = parent1.crossover(parent1, parent2)
            children.append(child)

        mutated = []
        for chrom in children+selected:
            chrom2 = chrom.mutate()
            mutated.append(max(chrom, chrom2))

        return self.__class__(mutated)

    def mean_score(self) -> float:
        s = sum(chromosome.score for chromosome in self.population)
        return s / self.len_pop


class GeneticAlgo(Generic[Chrom]):

    def __init__(self,
                 extract_sol: Callable[
                     [PopulationABC[Chrom]], list[Chrom]],
                 between_generations: Optional[Callable[
                     [PopulationABC[Chrom], list[Chrom], int], None]] = None
                 ):
        self.extract_sol = extract_sol
        self.between_generations = between_generations
        self.nb_gen = 0
        self.last_population = None

    def main_algo(self, starting_pop: PopulationABC[Chrom])\
            -> List[Chrom]:
        population = starting_pop
        solutions = self.extract_sol(population)
        self.nb_gen = 0
        while not solutions:
            population = population.new_generation()
            self.last_population = population
            solutions = self.extract_sol(population)
            self.nb_gen += 1
            if self.between_generations is not None:
                self.between_generations(population, solutions, self.nb_gen)
        return solutions
