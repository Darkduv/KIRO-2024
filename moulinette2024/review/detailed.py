"""Detailed constraints."""

# import matplotlib.pyplot as plt
from model import *


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


def reseq_cost1(inst: Instance, sol: Solution):
    betweens = (
        (sol.body_exit, sol.paint_entry, inst.body_shop.resequencing_lag),
    )
    ss = 0
    for s1, s2, lag in betweens:
        ss += cost_between_shops(lag, s1, s2)
    return ss * inst.parameters.resequencing_cost


def reseq_cost2(inst: Instance, sol: Solution):
    betweens = (
        (sol.paint_exit, sol.assembly_entry, inst.paint_shop.resequencing_lag),
    )
    ss = 0
    for s1, s2, lag in betweens:
        ss += cost_between_shops(lag, s1, s2)
    return ss * inst.parameters.resequencing_cost


def lot_changes_cost(inst: Instance, sol: Solution, const: Constraint):
    ss = 0
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    partitions = {}
    for i, group in enumerate(const.partition):
        for a in group:
            partitions[a] = i
    sigma = shops[const.shop]
    for v1, v2 in zip(sigma, sigma[1:]):
        if partitions[v1] != partitions[v2]:
            ss += const.cost
    return ss


def sum_batches(ll: list, size: int):
    return [sum(ll[a:a+size]) for a in range(0, len(ll)-size+1)]


def rolling_cost(inst: Instance, sol: Solution, const: RollingWindowConstraint):
    ss = 0
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    sigma = shops[const.shop]
    val = [v in const.vehicles for v in sigma]
    violations = sum(
        max(0, batch-const.max_vehicles)**2
        for batch in sum_batches(val, const.window_size)
    )
    return const.cost * violations


def batch_sizes_cost(inst: Instance, sol: Solution, const: BatchSizeConstraint):
    shops = {
        "body": sol.body_entry,
        "paint": sol.paint_entry,
        "assembly": sol.assembly_entry,
    }
    sigma = shops[const.shop]
    batches = [0]
    for v in sigma:
        if v in const.vehicles:
            batches[-1] += 1
        elif batches[-1] != 0:
            batches.append(0)
    ss_b = 0
    for batch in batches:
        if batch == 0:
            continue
        ss_b += max(0, const.min_vehicles - batch, batch - const.max_vehicles)**2
    return ss_b * const.cost


cost_constraint = {
    BatchSizeConstraint: batch_sizes_cost,
    LotChangeConstraint: lot_changes_cost,
    RollingWindowConstraint: rolling_cost,
}


def score_const(
    instance: Instance,
    solution: Solution,
) -> int:
    if not verif_reseq(instance, solution):
        return 9999999999999999999999999
    dd = {}
    dd["reseq Body->Paint"] = reseq_cost1(instance, solution)
    dd["reseq Paint->Assem"] = reseq_cost2(instance, solution)
    for const in instance.constraints:
        ff = cost_constraint[const.__class__]
        dd[f"n°{const.id:2} type {const.__class__.__name__}"] = ff(instance, solution, const)
    ll = list(dd.items())
    return sorted(ll, key=lambda ab: ab[1], reverse=True)


def review(instance: Instance, solution: Solution):
    """Do nothing."""
    ll = score_const(instance, solution)
    for id_, score in ll:
        print(f"{id_:40}: {score:10}")
    # todo: implement
