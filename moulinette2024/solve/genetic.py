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
                key=lambda indiv:self.fitness(indiv)
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
        

###############################################################################
from model import *
from tools import chrono, Bar

from collections import defaultdict

class GeneticStation(GeneticAlgorithm):

    def fitness(self, individual: Solution) -> float:
        return judge.score(GeneticStation.INST, individual)
    
    def crossover(self, indiv1: Solution, indiv2: Solution) -> Solution:
        substationlist = indiv1.substations+indiv2.substations
        substationlist = list(set([s.id for s in substationlist]))

        i1s = len(indiv1.substations)
        i2s = len(indiv2.substations)
        retenir=int(random.uniform(i1s, i2s))

        substationlist = random.choices(
            substationlist, 
            k=retenir,
        )

        substa = []
        for s in substationlist : 
            if s in [_s.id for _s in indiv1.substations] : 
                station :Substation= [
                    sta 
                    for sta in indiv1.substations
                    if sta.id == s
                ][0]
            else:
                station :Substation= [
                    sta 
                    for sta in indiv2.substations
                    if sta.id == s
                ][0]
            typesta = station.substation_type
            typeca = station.land_cable_type
            substa.append(
                Substation(
                    id=s,
                    land_cable_type=typeca,
                    substation_type=typesta,
                )
            )
        turbines=[]
        for t in indiv1.turbines :
            wt = WindTurbine.by_id(t.id)
            def dist(s):
                t=wt
                return (t.x-s.x)**2+(t.y-s.y)**2
            s_min = min([SubstationLocation.by_id(s.id) for s in substa], key=dist)
            turbines.append(
                Turbine(
                    id=t.id,
                    substation_id=s_min.id,
                )
            )
        
        cables =[]
        for s in substa : 
            if random.random()>0.5:
                cables.append(
                    SubstationSubstationCable(
                        substation_id=s.id,
                        other_substation_id=random.choice(
                            [station.id for station in substa]
                        ),
                        cable_type=random.choice(
                            [cable.cable_type for cable in indiv1.substation_substation_cables]
                        )
                    )
                )
                

        return Solution(
            substations=substa,
            turbines=turbines,
            substation_substation_cables=cables,
        )

    
    def mutate(self, indiv1: Solution) -> Solution:
        return indiv1

@chrono
def solve(instance: Instance):
    nbpop = 50
    nbgenerations = 2
    mutationrate = 0.05

    def randomguy():
        substa=[]
        for s in instance.substation_locations:
            if random.random()>0.5 : 
                substa.append(
                    Substation(
                        id=s.id,
                        land_cable_type=random.choice(
                            [cabletype.id for cabletype in instance.land_substation_cable_types],

                        ),
                        substation_type=random.choice(
                            [stationtype.id for stationtype in instance.substation_types]
                        )
                    )
                )
        turbines = []
        for turbine in instance.wind_turbines:
            turbines.append(
                Turbine(
                    id=turbine.id,
                    substation_id=random.choice(
                        [station.id for station in substa]
                    ),
                )
            )
        
        cables =[]
        for s in substa : 
            if random.random()>0.5:
                cables.append(
                    SubstationSubstationCable(
                        substation_id=s.id,
                        other_substation_id=random.choice(
                            [station.id for station in substa]
                        ),
                        cable_type=random.choice(
                            [cabletype.id for cabletype in instance.substation_substation_cable_types]
                        )
                    )
                )
    
        return Solution(
            turbines=turbines,
            substations=substa,
            substation_substation_cables=cables,
        )

    initialpop = [randomguy() for _ in range(nbpop)]

    algo = GeneticStation(
        initial_population=initialpop,
        number_of_best_indiv=nbpop//4,
    )

    GeneticStation.INST = instance

    algo.compute_generations(number_of_generations_to_compute=nbgenerations)

    return algo.best_individuals()[max(algo.best_individuals())]



    

    



    
    

