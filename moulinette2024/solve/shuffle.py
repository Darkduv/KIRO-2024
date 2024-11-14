"""Default, empty solver implementation."""

from model import (
    Instance, Solution, VehicleType
)
from tools import chrono, Bar

from model.judge import reseq_2tones

from collections import defaultdict

from random import shuffle


@chrono
def solve(instance: Instance)->Solution:
    """Compute nothing."""
    ## TODO TODO le default

    initial_order_vehicles = [v.id for v in instance.vehicles]
    shuffle(initial_order_vehicles) 
    
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
