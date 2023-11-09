"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    ## TODO TODO le default

    substation_type = instance.substation_types[0].id
    to_mainland_cable_type = instance.land_substation_cable_types[0].id
    substation_loc = instance.substation_locations[0].id
    substations = [Substation(substation_loc, to_mainland_cable_type, substation_type)]

    turbines = [Turbine(wind_turbine.id, substation_loc) for wind_turbine in instance.wind_turbines]

    sol = Solution(turbines,substations, [])

    return sol
