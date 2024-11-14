"""Solution scoring and verification."""

# import numpy as np
from .definitions import *


def reseq_2tones(sigma: list[int], two_tones: list[int], delta: int) -> list[int]:
    sigma = sigma[:]
    two_tones = set(two_tones)
    i = 0
    while i < len(sigma):
        v = sigma[i]
        if v not in two_tones:
            i += 1
            continue
        two_tones.remove(v)
        sigma[i:i+delta+1] = sigma[i+1:i+delta+1]+sigma[i:i+1]
    return sigma


def sigma_moins_1(sigma: list[int]) -> list[int]:
    """Renvoie sigma -1"""
    l2 = sorted(((v, i) for i, v in enumerate(sigma, start=1)))
    return [i for _, i in l2]


def get_two_tones(ll: list[Vehicle]) -> list[int]:
    return [v.id for v in ll if v.type == VehicleType.TWOTONE]


def verif_reseq(inst: Instance, sol: Solution):
    if sol.assembly_entry != sol.assembly_exit:
        return False
    if sol.body_entry != sol.body_exit:
        return False
    two_tones = get_two_tones(inst.vehicles)
    paint_exit = reseq_2tones(sol.paint_entry, two_tones, inst.parameters.two_tone_delta)
    return paint_exit == sol.paint_exit

def cost_between_shops(lag: int, sigma_out1: list[int], sigma_in2:list[int]):
    ss = 0
    for t1, t2 in zip(sigma_moins_1(sigma_out1), sigma_moins_1(sigma_in2)):
        ss += max(0, t1 - lag - t2)
    return ss


def reseq_cost(inst: Instance, sol: Solution):
    betweens = (
        (sol.body_exit, sol.paint_entry, inst.body_shop.resequencing_lag),
        (sol.paint_exit, sol.assembly_entry, inst.paint_shop.resequencing_lag),
    )
    ss = 0
    for s1, s2, lag in betweens:
        ss += cost_between_shops(lag, s1, s2)
    return ss * inst.parameters.resequencing_cost


def lot_changes_cost(inst: Instance, sol: Solution):
    ss = 0
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    for constraint in inst.constraints:
        if not isinstance(constraint, LotChangeConstraint):
            continue
        partitions = {}
        for group in constraint.partitions:
            for a in group:
                partitions[a] = set(group)
        sigma = shops[constraint.shop]
        for v1, v2 in zip(sigma, sigma[1:]):
            if partitions[v1] != partitions[v2]:
                ss += constraint.cost
    return ss


def sum_batches(ll: list, size: int):
    return [sum(ll[a:a+size]) for a in range(0, len(ll)-size+1)]


def rolling_cost(inst: Instance, sol: Solution):
    ss = 0
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    for constraint in inst.constraints:
        if not isinstance(constraint, RollingWindowConstraint):
            continue
        sigma = shops[constraint.shop]
        val = [v in constraint.vehicles for v in sigma]
        violations = max(0, sum_batches(val, constraint.window_size)-constraint.max_vehicles)
        ss += constraint.cost * violations ** 2
    return ss


def batch_sizes_cost(inst: Instance, sol: Solution):
    ss = 0
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    for constraint in inst.constraints:
        if not isinstance(constraint, BatchSizeConstraint):
            continue
        sigma = shops[constraint.shop]
        batches = [0]
        for v in sigma:
            if v in constraint.vehicles:
                batches[-1] += 1
            elif batches[-1] != 0:
                batches.append(0)
        ss_b = 0
        for batch in batches:
            if batch == 0:
                continue
            ss_b += max(0, constraint.min_vehicles - batch, batch - constraint.max_vehicles)**2
        ss += ss_b * constraint.cost
    return ss


def score(
    instance: Instance,
    solution: Solution,
) -> int:
    if not verif_reseq(instance, solution):
        return 9999999999999999999999999
    total_cost = 0
    total_cost += reseq_cost(instance, solution)
    total_cost += lot_changes_cost(instance, solution)
    total_cost += rolling_cost(instance, solution)
    total_cost += batch_sizes_cost(instance, solution)
    return total_cost

