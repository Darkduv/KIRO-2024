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
        mutation_rate:float,
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

        #Probabilité de mutation
        self.mutation_rate= mutation_rate
    
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
    
    def best_individual_last_generation(self, )->Any:
        return max(
            self.generations[max(self.generations)],
            key=lambda indiv:self.fitness(indiv)
        )

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
from sklearn.cluster import AgglomerativeClustering

from collections import defaultdict

def simplify_instance(
    instance:Instance,
    nb_senarii_final:int,
)->Instance:
    """Simplifie les scénarios de vent d'une instance pour simplifier les 
    itérations.
    """
    scenarii=instance.wind_scenarios
    powers_and_probabilities=np.array(
        [
            [scenario.power_generation, scenario.probability]
            for scenario in scenarii
        ]
    )
    clusterisation=AgglomerativeClustering(
        n_clusters=nb_senarii_final,
        linkage='single',
    ).fit(powers_and_probabilities)

    new_wind_scenarii = []
    for n_cluster in range(nb_senarii_final):
        labelized_wind=[
            scenario 
            for i, scenario in enumerate(instance.wind_scenarios) 
            if clusterisation.labels_[i]==n_cluster
        ]
        total_probability=sum(
            [
                scenario.probability
                for scenario in labelized_wind
            ]
        )

        mean_power=sum(
            [
                scenario.power_generation*scenario.probability
                for scenario in labelized_wind
            ]
        )/total_probability

        new_wind_scenarii.append(
            WindScenario(
                power_generation=mean_power,
                probability=total_probability,
                id=1e6+n_cluster,
            )
        )

    return Instance(
        land_substation_cable_types=instance.land_substation_cable_types,
        wind_turbines=instance.wind_turbines,
        wind_scenarios=new_wind_scenarii,
        substation_locations=instance.substation_locations,
        general_parameters=instance.general_parameters,
        substation_substation_cable_types=instance.substation_substation_cable_types,
        substation_types=instance.substation_types
    )



class TopologicalGenetic(GeneticAlgorithm):
    
    instance:Instance=None
    simplified_instance:Instance= None
    true_fitness_every:int=30
    minimal_number_substation:int=1
    fintess_calls:int=0
    simpl_fitness_calls:int=0

    def fitness(self, individual: Solution) -> float:
        TopologicalGenetic.fintess_calls+=1
        return -score(instance=TopologicalGenetic.instance, solution=individual)
    
    def simplified_fitness(self, individual: Solution)->float:
        TopologicalGenetic.simpl_fitness_calls+=1
        return -score(instance=TopologicalGenetic.simplified_instance, solution=individual)
    
    def select_best_individuals(
        self, 
    )->list:
        """Renvoie les X meilleurs individus pour la dernière génération

        Returns:
            list[Any]: Meilleurs individus retenus
        """
        if (max(self.generations)%TopologicalGenetic.true_fitness_every)==0:
            print(max(self.generations), 'fitness')
            fitness=self.fitness
        else:
            print(max(self.generations), 'simplified')
            fitness=self.simplified_fitness

        return sorted(
            [
                indiv
                for indiv in self.last_generation
            ],
            key=fitness,
            reverse=True
        )[:self.number_best_indiv]

    def crossover(self, indiv1: Solution, indiv2: Solution) -> Solution:
        # On trouve toutes les sous stations actives dans les deux solutions
        subids_all=set(indiv1.substations_ids+indiv2.substations_ids)
        # On trouve toutes les stations en commun, on va les garder
        subids_comm=set(indiv1.substations_ids).intersection(set(indiv2.substations_ids))
        # On trouve toutes les stations qui sont dans l'un mais pas l'autre 
        subids_1=subids_all.difference(set(indiv2.substations_ids))
        subids_2=subids_all.difference(set(indiv1.substations_ids))

        # Dans la nouvelle solution, on fait le choix de garder toutes les
        # stations en commun
        substations_to_keep = list(subids_comm)

        # Ensuite, on garde aléatoirement le reste
        for substaid in list(subids_1.union(subids_2)):
            if random.random()>0.5 or len(substations_to_keep)<self.minimal_number_substation:
                substations_to_keep.append(substaid)
        
        # Maintenant il faut trouver les types des cables et des substa corres
        # pondant, et on crossover dans le cas où c'est en commmun
        new_substas = []
        for substaid in substations_to_keep:
            if substaid in subids_1 :
                new_substas.append(
                    Substation(
                        id=substaid,
                        land_cable_type=indiv1.mainland_cable_types[substaid].id,
                        substation_type=indiv1.substations_types[substaid].id,
                    )
                )
            elif substaid in subids_2 :
                new_substas.append(
                    Substation(
                        id=substaid,
                        land_cable_type=indiv2.mainland_cable_types[substaid].id,
                        substation_type=indiv2.substations_types[substaid].id,
                    )
                )
            else:
                assert substaid in subids_comm
                if random.random()>0.5:
                    lct=indiv1.mainland_cable_types[substaid].id
                else:
                    lct=indiv2.mainland_cable_types[substaid].id
                if random.random()>0.5:
                    st=indiv1.substations_types[substaid].id
                else:
                    st=indiv2.substations_types[substaid].id
                new_substas.append(
                    Substation(
                        id=substaid,
                        land_cable_type=lct,
                        substation_type=st,
                    )
                )
        
        newsubstaids=[s.id for s in new_substas]
        
        # Pour chaque turbine, on va relier à la substation la plus proche
        new_turbines=[]
        for turbine in indiv1.turbines:
            closestsubsta = min(
                {
                    theid: thedist
                    for theid, thedist in self.instance.distance_of_turbine_to_substation[turbine.id].items()
                    if theid in newsubstaids
                },
                key=lambda thekey: self.instance.distance_of_turbine_to_substation[turbine.id][thekey]
            )
            new_turbines.append(
                Turbine(
                    id=turbine.id, 
                    substation_id=closestsubsta,
                )
            )
        
        #Pour l'instant on ne génère pas de câbles entre les sousstations
        subsubcable=[]

        # if len(new_substas)>1 : print(len(new_substas))
        # On renvoie la solution 
        return Solution(
            turbines=new_turbines,
            substations=new_substas,
            substation_substation_cables=subsubcable,
        )

    
    def mutate(self, indiv1: Solution) -> Solution:
        # On commence par allumer des substas de manière aléatoire
        subids=indiv1.substations_ids
        allsubids=[loc.id for loc in self.instance.substation_locations]
        offsubs=[theid for theid in allsubids if not theid in subids]

        new_substas=[]
        for theid in offsubs:
            if random.random()<self.mutation_rate:
                new_substas.append(
                    Substation(
                        id=theid, 
                        land_cable_type=random.choice(
                            [
                                land.id
                                for land in self.instance.land_substation_cable_types
                            ]
                        ),
                        substation_type=random.choice(
                            [
                                typesub.id
                                for typesub in self.instance.substation_types
                            ]
                        ),
                    )
                )
        
        # On peut changer le type : 
        for substachange in indiv1.substations:
            if random.random()<self.mutation_rate:
                substachange.land_cable_type = random.choice(
                    [
                        land.id
                        for land in self.instance.land_substation_cable_types
                    ]
                )
            if random.random()<self.mutation_rate:
                substachange.substation_type = random.choice(
                    [
                        typesub.id
                        for typesub in self.instance.substation_types
                    ]
                )

        new_substas+=indiv1.substations
        newsubstaids=[s.id for s in new_substas]

        # On relie les éoliennes à la plus proche
        # Pour chaque turbine, on va relier à la substation la plus proche
        new_turbines=[]
        for turbine in indiv1.turbines:
            closestsubsta = min(
                {
                    theid: thedist
                    for theid, thedist in self.instance.distance_of_turbine_to_substation[turbine.id].items()
                    if theid in newsubstaids
                },
                key=lambda thekey: self.instance.distance_of_turbine_to_substation[turbine.id][thekey]
            )
            new_turbines.append(
                Turbine(
                    id=turbine.id, 
                    substation_id=closestsubsta,
                )
            )
        
        #Pour l'instant on ne génère pas de câbles entre les sousstations
        subsubcable=[]

        # if len(new_substas)>1 : print(len(new_substas))
        # On renvoie la solution 
        return Solution(
            turbines=new_turbines,
            substations=new_substas,
            substation_substation_cables=subsubcable,
        )
    
    @classmethod
    def random_init_solution(cls, )->Solution:
        """Activation d'une seule sous station"""
        substa_active = random.choice(
            [
                substa.id
                for substa in cls.instance.substation_locations
            ]
        )

        typesubta = random.choice(
            [
                typesub.id
                for typesub in cls.instance.substation_types
            ]
        )

        landcable=random.choice(
            [
                land.id
                for land in cls.instance.land_substation_cable_types
            ]
        )

        return Solution(
            turbines=[
                Turbine(id=windt.id, substation_id=substa_active)
                for windt in cls.instance.wind_turbines
            ],
            substations=[
                Substation(
                    id=substa_active,
                    substation_type=typesubta,
                    land_cable_type=landcable,
                )
            ],
            substation_substation_cables=[],
        )

    @classmethod
    def random_init_solution_multiple_substas(cls, nbsub:int)->Solution:
        subids=random.choices(cls.instance.substation_ids, k=min(nbsub, len(cls.instance.substation_locations)))
        new_subs = []
        for idsub in subids:
            new_subs.append(
                Substation(
                    id=idsub,
                    land_cable_type=random.choice(
                        [
                            land.id
                            for land in cls.instance.land_substation_cable_types
                        ]
                    ),
                    substation_type=random.choice(
                        [
                            typesub.id
                            for typesub in cls.instance.substation_types
                        ]
                    )
                )
            )
        
        new_turbines=[]
        for turbine in cls.instance.wind_turbines:
            closestsubsta = min(
                {
                    theid: thedist
                    for theid, thedist in cls.instance.distance_of_turbine_to_substation[turbine.id].items()
                    if theid in subids
                },
                key=lambda thekey: cls.instance.distance_of_turbine_to_substation[turbine.id][thekey]
            )
            new_turbines.append(
                Turbine(
                    id=turbine.id, 
                    substation_id=closestsubsta,
                )
            )
        
        subsubcable=[]

        # if len(new_substas)>1 : print(len(new_substas))
        # On renvoie la solution 
        return Solution(
            turbines=new_turbines,
            substations=new_subs,
            substation_substation_cables=subsubcable,
        )
        

    @classmethod
    def random_init_pop(cls, nb_pop:int, nbsubstasinit:int)->list[Solution]:
        if nbsubstasinit==1:
            return [TopologicalGenetic.random_init_solution() for _ in range(nb_pop)]
        else:
            return [TopologicalGenetic.random_init_solution_multiple_substas(nbsubstasinit) for _ in range(nb_pop)]

@chrono
def solve(instance: Instance):
    nbpop = 10
    nbgenerations = 1000
    mutationrate = 0.05

    TopologicalGenetic.instance = instance
    TopologicalGenetic.minimal_number_substation=1

    if len(instance.wind_scenarios)==1:
        TopologicalGenetic.true_fitness_every=1
    else:
        TopologicalGenetic.true_fitness_every= 5
        TopologicalGenetic.simplified_instance = simplify_instance(
            instance=instance, 
            # nb_senarii_final=3,
            nb_senarii_final=len(instance.wind_scenarios)//100+1,
        )

    
    algo = TopologicalGenetic(
        initial_population=TopologicalGenetic.random_init_pop(
            nb_pop=nbpop, 
            nbsubstasinit=len(instance.substation_locations)//2,
        ),
        number_of_best_indiv=nbpop//2,
        mutation_rate=mutationrate,
    )

    algo.compute_generations(number_of_generations_to_compute=nbgenerations)
    return algo.best_individual_last_generation()



    

    



    
    

