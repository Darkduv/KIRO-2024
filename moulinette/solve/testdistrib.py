# from functools import partial
# import math as m
# import numpy as np

from model import Instance, Solution
from review.default import review
from model import Prod, Distrib, Parameters, Command, score
from tools import chrono

from data import Driver

from random import randint, shuffle, random
from numpy import inf


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    driver = Driver("c")
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

    parameters = instance.parameters
    n_sites = len(instance.sites)
    print(f"Sum demand = {sum(client.demand for client in instance.clients)}")
    print(f"Capacité stockage = {capacity(parameters, Prod(1, 0)) * n_sites}")
    print(f"Ratio = {sum(client.demand for client in instance.clients) / (capacity(parameters, Prod(1, 0)) * n_sites)}")
    for _ in range(n_tot):
        if _ % int(n_tot / 10) == 0:
            print(f"ÉTAPE N°{_}")
        ratio = random() * 0.5 + 2.6
        n_sites = len(instance.sites)
        links = {}
        parameters = instance.parameters
        capacity_init = {site.id: capacity(parameters, Prod(site.id, 0)) * ratio for site in instance.sites}
        clients = instance.clients

        vide = randint(0, 4)
        moins = max(1, n_sites - vide)

        i_melange = list(range(n_sites))
        shuffle(i_melange)
        i_melange = i_melange[:moins]
        for client in clients:
            cl_id = client.id - 1
            s_min = 0
            mini = instance.s_c_distances[0][client.id - 1]
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
        # print(max(len(links[a]) for a in links), min(len(links[a]) for a in links),
        #       sum(len(links[a]) for a in links) / len(links), n_sites, len(instance.clients))
        distribs = []
        commands = []
        prods = []
        cu, c_costs = instance.parameters.capacity_cost, instance.parameters.capacities
        b_cost = instance.parameters.building_costs
        p_cost = instance.parameters.production_costs
        demands = {}
        for s in links:
            demand = 0
            for client in links[s]:
                demand += client.demand
                commands.append(Command(client.id, s))
            demands[s] = demand

        links = proche_voisin(instance)
        prods_fin = []
        distribs_fin = []
        l_demands = list(demands.keys())
        shuffle(l_demands)
        for s in l_demands:
            parent = links[s]
            if s in prods_fin:
                continue
            if (parent not in demands) or (parent in distribs_fin) or randint(1, 1000) < 895:
                prods_fin.append(s)
            else:
                # print("*", end="")
                demand = demands[s]
                demand_parent = demands[parent]
                stock_cost_diff = cu * penalty2(c_costs, demand, demand_parent)
                diff = b_cost.distrib - b_cost.prod + demand * p_cost.distrib + stock_cost_diff
                if diff > 0:
                    # print("***")
                    # print("yolo")
                    distribs.append(Distrib(s, parent))
                    distribs_fin.append(s)
                    demands[parent] += demand
                    if parent not in prods_fin:
                        prods_fin.append(parent)
                else:
                    # print()
                    prods_fin.append(s)
        ok = False
        for s in prods_fin:
            demand = demands[s]
            c_diff = b_cost.automation - demand * p_cost.automation + cu * penalty(c_costs, demand)
            if c_diff > 0:
                prods.append(Prod(s, 0))
            else:
                ok = True
                prods.append(Prod(s, 1))
        sol = Solution(prods, distribs, commands)
        sol_score = score(instance, sol, output=False)
        if sol_score < best_score:
            score(instance, sol, output=True)
            if ok:
                # print("yo")
                pass
            print(f"Étape n°{_} ;  New score : {sol_score}")
            best_score = sol_score
            best_solution = sol
            best_ratio = ratio
            best_vide = vide
            best_sites = i_melange
            best_clients = clients
            print(f"Score : {best_score} ; ratio = {best_ratio} ; vide = {best_vide}")
            print(f"Nb distrib : {len(sol.distribs)}")
    print(f"Score : {best_score} ; ratio = {best_ratio} ; vide = {best_vide}")
    # review(instance, solution)

    return best_solution


def penalty(c_costs, demand):
    c1 = max(demand - (c_costs.prod + 1 * c_costs.automation), 0)
    c2 = max(demand - (c_costs.prod + 0 * c_costs.automation), 0)
    return c1 - c2


def penalty2(c_costs, demand, demand_parent):
    c1 = max(demand - c_costs.prod, 0) + max(demand_parent - c_costs.prod, 0)
    c2 = max(demand + demand_parent - (c_costs.prod + 0 * c_costs.automation), 0)
    return c2 - c1


def proche_voisin(instance):
    links = {}
    for site in instance.sites:
        s_id = site.id - 1
        s_min = 0
        mini = instance.s_c_distances[0][s_id]
        for s, a in enumerate(instance.s_c_distances):
            if s == s_id:
                continue
            if a[s_id] < mini:
                s_min = s
                mini = a[s_id]
        s_min += 1
        links[site.id] = s_min
    return links


def capacity(parameters: Parameters, prod: Prod):
    return parameters.capacities.prod + prod.automation * parameters.capacities.automation
