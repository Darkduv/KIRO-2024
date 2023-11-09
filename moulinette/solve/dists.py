# from functools import partial
# import math as m
# import numpy as np

from model import *
from data import Driver
from tools import chrono

from numpy import inf
from random import shuffle, random, randint


@chrono
def solve(instance):
    """Compute nothing."""
    driver = Driver("d")
    solut = driver.retrieve()
    print("# ================== ")
    best_score = inf  # score(instance, solut, output=True)
    print(f"# Meilleur score = {best_score} ================== ")
    best_ratio = 0
    best_clients = []
    best_sites = []
    best_solution = None
    best_vide = 0
    n_tot = 5000
    for _ in range(n_tot):
        if _ % int(n_tot/10) == 0:
            print(f"ÉTAPE N°{_}")
        ratio = random()*0.6 + 2.5
        n_sites = len(instance.sites)
        links = {}
        parameters = instance.parameters
        capacity_init = {site.id: capacity(parameters, Prod(site.id, 0)) * ratio for site in instance.sites}
        clients = instance.clients

        vide = randint(0, 16)
        moins = max(1, n_sites - vide)

        i_melange = list(range(n_sites))
        shuffle(i_melange)
        i_melange = i_melange[:moins]
        for client in clients:
            cl_id = client.id - 1
            s_min = 0
            mini = instance.s_c_distances[0][cl_id]
            for s in i_melange:
                a = instance.s_c_distances[s]
                if a[cl_id] < mini and client.demand < capacity_init[s + 1]:
                    s_min = s
                    mini = a[cl_id]
                    capacity_init[s + 1] -= client.demand
            s_min += 1
            if s_min in links:
                links[s_min].append(client)
            else:
                links[s_min] = [client]
        distribs = []
        commands = []
        prods = []
        cu, c_costs = instance.parameters.capacity_cost, instance.parameters.capacities
        b_cost = instance.parameters.building_costs
        p_cost = instance.parameters.production_costs
        for s in links:
            demand = 0
            for client in links[s]:
                demand += client.demand
                commands.append(Command(client.id, s))
            c_diff = b_cost.automation - demand * p_cost.automation + cu * penalty(c_costs, demand)
            if c_diff > 0:
                prods.append(Prod(s, 0))
            else:
                prods.append(Prod(s, 1))
        sol = Solution(prods, distribs, commands)
        sol_score = score(instance, sol, output=False)
        if sol_score < best_score:
            score(instance, sol, output=True)
            print(f"Étape n°{_} ;  New score : {sol_score}")
            best_score = sol_score
            best_solution = sol
            best_ratio = ratio
            best_vide = vide
            best_sites = i_melange
            best_clients = clients
            print(f"Score : {best_score} ; ratio = {best_ratio} ; vide = {best_vide}")
    print(f"Score : {best_score} ; ratio = {best_ratio} ; vide = {best_vide}")
    return best_solution


def capacity(parameters: Parameters, prod: Prod):
    return parameters.capacities.prod + prod.automation * parameters.capacities.automation


def penalty(c_costs, demand):
    c1 = max(demand - (c_costs.prod + 1 * c_costs.automation), 0)
    c2 = max(demand - (c_costs.prod + 0 * c_costs.automation), 0)
    return c1 - c2
