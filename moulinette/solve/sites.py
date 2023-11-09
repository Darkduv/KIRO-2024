from functools import partial
import math as m
import numpy as np

from model import *
from tools import chrono


@chrono
def solve(instance):
    """Compute nothing."""
    i = 0
    n_sites = len(instance.sites)
    site = instance.sites[i]
    prod = Prod(site.id, 1)
    cap = capacity(instance.parameters, prod)
    prods = [prod]
    distribs = []
    commands = []
    demand = 0
    for client in instance.clients:
        demand += client.demand
        if demand > cap and i + 1 < n_sites:
            i += 1
            prod = Prod(instance.sites[i].id, 1)
            prods.append(prod)
            cap = capacity(instance.parameters, prod)
            demand = client.demand
        commands.append(Command(client.id, prod.id))
    return Solution(prods, distribs, commands)


def capacity(parameters: Parameters, prod: Prod):
    return parameters.capacities.prod + prod.automation*parameters.capacities.automation
