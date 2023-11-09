import numpy as np
import random
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any
from collections import defaultdict

class GeneticAlgorithm(ABC):

    def __init__(
        self,
        initial_population:list,
        number_of_best_indiv:int,
    ):
        
        # Population de départ
        self.initial_population = initial_population

        # Générations successives
        self.generations : dict[int, list] = defaultdict(list)
        self.generations[0] = self.initial_population

        # Nombre d'individus à garder
        self.number_best_indiv = (number_of_best_indiv//2)*2

        # Nombre d'individus dans la population 
        self.number_indiv = len(self.initial_population)
    
    @property
    def last_generation(self, ):
        return self.generations[max(self.generations.keys())]
    
    def best_individuals(self,)->dict[int, Any]:
        """Renvoie les meilleurs individus par génération
        """
        return {
            generation:max(
                self.generations[generation],
                key=lambda indiv:self.fitness()
            )
            for generation in self.generations.keys()
        }

    @abstractmethod
    def fitness(self, individual:Any)->float:
        """Renvoie le score d'un inidividu.

        Args:
            individual (Any): Un individu

        Returns:
            float: Fitness score
        """
        pass

    @abstractmethod
    def crossover(self, indiv1:Any, indiv2:Any)->Any:
        """Renvoie un nouvel individu à partir de deux parents

        Args:
            indiv1 (Any): Parent 1
            indiv2 (Any): Parent 2

        Returns:
            Any: L'enfant
        """
        pass

    @abstractmethod
    def mutate(self, indiv1:Any)->Any:
        """Crée et renvoie un individu muté

        Args:
            indiv1 (Any): Individu à muter

        Returns:
            Any: Individu muté
        """
        pass
    
    def select_best_individuals(
        self, 
    )->list:
        """Renvoie les X meilleurs individus pour la dernière génération

        Returns:
            list[Any]: Meilleurs individus retenus
        """
        return sorted(
            [
                indiv
                for indiv in self.last_generation
            ],
            key=lambda indiv:self.fitness(individual=indiv),
            reverse=True
        )[:self.number_best_indiv]
    
    def compute_next_generation(self, )->None:
        """Calcule la prochaine génération et la stocke
        """
        best_individuals:list = self.select_best_individuals()

        new_generation = [indiv for indiv in best_individuals]

        while len(new_generation) < self.number_indiv :
            parent1, parent2 = random.choices(best_individuals, k=2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_generation.append(child)
        
        self.generations[max(self.generations.keys())+1] = new_generation
    
    def compute_generations(
        self, 
        number_of_generations_to_compute : int,
    )->None:
        """Calcule X nouvelles générations

        Args:
            number_of_generations_to_compute (int): Nombre de calculs à faire
        """
        for _ in range(number_of_generations_to_compute) :
            self.compute_next_generation()
        



    
    

