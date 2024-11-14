"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar

from collections import defaultdict


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    ## TODO TODO le default

    dic_station_y = {station.y: station.id for station in instance.substation_locations}
    dic_turbine_y = defaultdict(list)
    for turbine in instance.wind_turbines:
        dic_turbine_y[turbine.y].append(turbine.id)

    turb_to_stat = {}
    for y in dic_turbine_y:
        _, ys_min = min((abs(y-ys),ys) for ys in dic_station_y)
        turb_to_stat[y] = ys_min

    substation_type = instance.substation_types[0].id
    to_mainland_cable_type = instance.land_substation_cable_types[0].id
    substation_loc = instance.substation_locations[0].id
    substations = [Substation(dic_station_y[yy], to_mainland_cable_type, substation_type) for yy in set(turb_to_stat.values())]

    turbines = [Turbine(wind_turbine.id, dic_station_y[turb_to_stat[wind_turbine.y]]) for wind_turbine in instance.wind_turbines]

    sol = Solution(turbines,substations, [])

    return sol
