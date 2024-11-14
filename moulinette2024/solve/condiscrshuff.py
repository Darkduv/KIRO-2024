
from model import (
    Instance, Solution, VehicleType, LotChangeConstraint, RollingWindowConstraint, BatchSizeConstraint
)
from tools import chrono
from random import shuffle

from model.judge import reseq_2tones, score

def simply_reseq(instance:Instance, order : list[int])->Solution:
    initial_order_vehicles = order
    
    two_tones = [v.id for v in instance.vehicles if v.type == VehicleType.TWOTONE]

    post_paint_order_vehicles = reseq_2tones(
        sigma=initial_order_vehicles,
        two_tones=two_tones,
        delta=instance.parameters.two_tone_delta,
    )

    sol = Solution(
        body_entry=initial_order_vehicles,
        body_exit=initial_order_vehicles,
        paint_entry=initial_order_vehicles,
        paint_exit=post_paint_order_vehicles,
        assembly_entry=post_paint_order_vehicles,
        assembly_exit=post_paint_order_vehicles,
    )

    return sol

# def shuffle_between(instance:Instance, order:list[int])->Solution:
#     initial_order_vehicles = order
    
#     two_tones = [v.id for v in instance.vehicles if v.type == VehicleType.TWOTONE]

#     pre_paint = shuffle(order)

#     post_paint = reseq_2tones(
#         sigma=pre_paint,
#         two_tones=two_tones,
#         delta=instance.parameters.two_tone_delta,
#     )

#     pre_ass = shuffle(order)

#     sol = Solution(
#         body_entry=initial_order_vehicles,
#         body_exit=initial_order_vehicles,
#         paint_entry=pre_paint,
#         paint_exit=post_paint,
#         assembly_entry=pre_ass,
#         assembly_exit=pre_ass,
#     )

#     return sol

def optimal_lot_order(instance:Instance, lot_contraint:LotChangeConstraint)->list[int]:
    order = []

    for p in lot_contraint.partition :
        shuffle(p)
        order += p

    
    for v in instance.vehicles:
        if v.id not in order : 
            order.append(v.id)

    return order

def optimal_window_order(instance:Instance, window_contraint:RollingWindowConstraint)->list[int]:

    vehicles_in_cons = list(set(window_contraint.vehicles))

    other_vehicle = list(set([v.id for v in instance.vehicles if v.id not in vehicles_in_cons]))

    ratio_other = round(len(other_vehicle)/len(vehicles_in_cons))
    ratio_cons = round(len(vehicles_in_cons)/len(other_vehicle))

    depop_in_cons = [i for i in vehicles_in_cons]
    shuffle(depop_in_cons)
    depop_in_other = [i for i in other_vehicle]
    shuffle(depop_in_other)
    solution = []

    if ratio_cons > 0 :
        big = depop_in_cons
        small = depop_in_other
    else:
        big = depop_in_other
        small = depop_in_cons
    
    ratio = ratio_cons if ratio_cons>0 else ratio_other

    while big and small :
        batch_big = big[:ratio]
        big = big[ratio:]
        solution += batch_big
        solution += small[:1]
        small = small[1:]

    for v in instance.vehicles:
        if v.id not in solution : 
            solution.append(v.id)

    return solution

def optimal_batch_order(instance:Instance, batch_constraint:BatchSizeConstraint, mini_ensemble:int=1)->list[int]:

    vehicles_in_cons = list(set(batch_constraint.vehicles))

    other_vehicle = list(set([v.id for v in instance.vehicles if v.id not in vehicles_in_cons]))

    ratio_other = round(len(other_vehicle)/len(vehicles_in_cons))
    ratio_cons = round(len(vehicles_in_cons)/len(other_vehicle))

    depop_in_cons = [i for i in vehicles_in_cons]
    shuffle(depop_in_cons)
    depop_in_other = [i for i in other_vehicle]
    shuffle(depop_in_other)
    solution = []

    if ratio_cons > 0 :
        big = depop_in_cons
        small = depop_in_other
    else:
        big = depop_in_other
        small = depop_in_cons
    
    ratio = ratio_cons if ratio_cons>0 else ratio_other

    while big and small :
        batch_big = big[:ratio]
        big = big[ratio:]
        solution += batch_big
        solution += small[:1]
        small = small[1:]

    for v in instance.vehicles:
        if v.id not in solution : 
            solution.append(v.id)

    return solution

@chrono
def solve(instance: Instance)->Solution:

    # --- On veut travailler sur l'ordre initial qu'on file à body

    # Trouver toutes les contraintes de body par type

    constraints = instance.constraints

    lot_constraints = [c for c in constraints if isinstance(c, LotChangeConstraint) and c.shop=="body"]
    window_constraints = [c for c in constraints if isinstance(c, RollingWindowConstraint) and c.shop=="body"]
    batch_constraints = [c for c in constraints if isinstance(c, BatchSizeConstraint) and c.shop=="body"]

    # Trouver les pires contraintes
    worst_lot = None
    worst_window = None
    worst_batch = None

    if lot_constraints :
        worst_lot = max(lot_constraints, key=lambda lc: lc.cost * len(lc.partition))
    if window_constraints :
        worst_window = max(window_constraints, key=lambda wc: wc.cost*(wc.window_size-wc.max_vehicles)**2)
    if batch_constraints :
        worst_batch = max(batch_constraints, key=lambda bc: bc.cost*(bc.min_vehicles)/(bc.max_vehicles-bc.min_vehicles)**1.5)

    # Trouver les solutions optimales pour body (3 au max)
    solu_lot = None
    solu_window = None
    solu_batch = None
    _score = 1e9
    _best_sol = None

    if worst_lot :
        solu_lot = optimal_lot_order(instance=instance, lot_contraint=worst_lot)
        assemble_reseq = simply_reseq(instance=instance, order=solu_lot)
        score_2 = score(instance, assemble_reseq)
        if score_2 < _score : 
            _best_sol = assemble_reseq
            _score = score_2
            print(_score)

    if worst_batch :
        solu_batch = optimal_batch_order(instance=instance, batch_constraint=worst_batch)
        assemble_reseq = simply_reseq(instance=instance, order=solu_batch)
        score_2 = score(instance, assemble_reseq)
        if score_2 < _score : 
            _best_sol = assemble_reseq
            _score = score_2
            print(_score)

    if worst_window :
        solu_window = optimal_window_order(instance=instance, window_contraint=worst_window)
        assemble_reseq = simply_reseq(instance=instance, order=solu_window)
        score_2 = score(instance, assemble_reseq)
        if score_2 < _score : 
            _best_sol = assemble_reseq
            _score = score_2
            print(_score)

    # renvoyer la solution
    return _best_sol if _best_sol else simply_reseq(instance, [v.id for v in instance.vehicles])
