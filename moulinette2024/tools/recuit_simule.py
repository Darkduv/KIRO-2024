from math import cos, sin, exp, pi
import random
from typing import Callable, Any

# Algorithme du recuit simulé
def recuit_simule(
    initial_solution    :   Any,
    initial_temperature :   float,
    cooling_rate        :   float,
    num_iterations      :   int,
    energy_function     :   Callable,
    neighbour_function  :   Callable,
)->tuple[Any, float]:
    """Algorithme du recuit simulé. Renvoie la meilleure solution et son 
    énergie.

    Args:
        initial_solution (Any): Solution initiale.
        initial_temperature (float): Température initiale. 
            Strictement supérieur à 0.
        cooling_rate (float): Coefficient multiplicatif de la température à
            chaque itération. Entre 0 et 1 strictement.
        num_iterations (int): Nom d'itérations
        energy_function (Callable): Fonction qui renvoie l'énergie. Prend 
            un objet du type d'initial_solution et renvoie un float
        neighbour_function (Callable): Fonction qui renvoie un voisin d'un 
            objet du type d'initial solution à partir d'un objet du même type.

    Returns:
        tuple[Any, float]: Meilleure solution, son énergie
    """
    current_solution = initial_solution
    current_energy = energy_function(current_solution)

    current_temperature = initial_temperature

    best_solution = current_solution
    best_energy = current_energy

    for iteration in range(num_iterations):

        # Choix d'une solution voisine
        neighbor_solution = neighbour_function(current_solution)
        neighbor_energy = energy_function(neighbor_solution)

        # Calcul de la différence d'énergie
        delta_energy = neighbor_energy - current_energy

        # Acceptation de la nouvelle solution en fonction de 
        # la température et de la différence d'énergie
        if delta_energy < 0 or random.random() < exp(-delta_energy / current_temperature):
            current_solution = neighbor_solution
            current_energy = neighbor_energy

            # Mettre à jour la meilleure solution trouvée
            if current_energy < best_energy:
                best_solution = current_solution
                best_energy = current_energy

        # Refroidissement (diminution de la température)
        current_temperature *= cooling_rate

    return best_solution, best_energy





# ###################################################### EXEMPLE

if __name__ == "__main__":
    initial_solution = random.uniform(-10, 10)
    initial_temperature = 10000
    cooling_rate = 0.95
    num_iterations = 100000

    def energy_float(x:float):
        return sin(x) + 0.5 * cos(2 * x) + 0.2 * sin(5 * x) +0.1*sin(8*x)
    def energy_list(x:list[float]):
        return sum([energy_float(element) for element in x])
    
    def neighbour_float(x:float):
        return x+0.1*random.random()
    
    def neighbour_list(x:list[float]):
        return [neighbour_float(element) for element in x]

    best_solution, best_energy = recuit_simule(
        initial_solution=0.0, 
        initial_temperature=initial_temperature, 
        cooling_rate=cooling_rate, 
        num_iterations=num_iterations,
        energy_function=energy_float,
        neighbour_function=neighbour_float,
    )

    print("Meilleure solution trouvée :", best_solution/pi)
    print("Énergie de la meilleure solution :", best_energy)