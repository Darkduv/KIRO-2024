"""Default, empty instance visualization tool."""

import matplotlib.pyplot as plt
from model import *


def str_lot_change(const: LotChangeConstraint) -> str:
    return f"n°{const.id:2} : cost={const.cost:6}, len groups partition={sorted(len(a) for a in const.partition)}"

def str_batchsize(const: BatchSizeConstraint) -> str:
    return f"n°{const.id:2} : cost={const.cost:6}, {const.min_vehicles:1} <= size <= {const.max_vehicles:3}, nb vehicles={len(const.vehicles)}"

def str_rolling(const: RollingWindowConstraint) -> str:
    return f"n°{const.id:2} : cost={const.cost:6}, Mr={const.max_vehicles:2}, window={const.window_size:2}, nb_vehicles={len(const.vehicles)}"


def view(instance: Instance, keep_empty: bool = False):
    lot_consts = [constraint for constraint in instance.constraints if isinstance(constraint, LotChangeConstraint)]
    batch_consts = [constraint for constraint in instance.constraints if isinstance(constraint, BatchSizeConstraint)]
    rolling_consts = [constraint for constraint in instance.constraints if isinstance(constraint, RollingWindowConstraint)]

    consts = {
        "LotChange": (lot_consts, str_lot_change),
        "BatchSize": (batch_consts, str_batchsize),
        "RolliWind": (rolling_consts, str_rolling),
    }
    for type_const, (ll, f_str) in consts.items():
        if not keep_empty and not ll:
            continue
        print(f"Looking at Constraints of type ==>> {type_const}  <<==, there are {len(ll)} of them")
        shops = {
            "body": [],
            "paint": [],
            "assembly": [],
        }
        for const in ll:
            shops[const.shop].append(const)
        for shop, ll in shops.items():
            if not keep_empty and not ll:
                continue
            print(f"   on shop {shop:10}, {len(ll):2} constraints :")
            for const in ll:
                print("      - ", f_str(const))


