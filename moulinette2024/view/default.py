"""Default, empty instance visualization tool."""

import matplotlib.pyplot as plt
from model import *



def view(instance: Instance):
    lot_consts = [constraint for constraint in instance.constraints if isinstance(constraint, LotChangeConstraint)]
    batch_consts = [constraint for constraint in instance.constraints if isinstance(constraint, BatchSizeConstraint)]
    rolling_consts = [constraint for constraint in instance.constraints if isinstance(constraint, RollingWindowConstraint)]
    print("| Vehicles | Constraints | 2t cost | reseq cost || constraints || lot change | batchsize | rolling |")
    print(f"| {len(instance.vehicles):8} | {len(instance.constraints):11}"
          f" | {instance.parameters.two_tone_delta:7} | {instance.parameters.resequencing_cost:10}"
          f" || {len(instance.constraints):11} || {len(lot_consts):10} | {len(batch_consts):9} | {len(rolling_consts):7} |")

