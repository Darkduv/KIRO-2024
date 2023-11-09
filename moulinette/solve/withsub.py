"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar

from collections import defaultdict


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    ## TODO TODO le default


    lll = []
    for station_type in instance.substation_types:
        for cable_type in instance.land_substation_cable_types:
            lll.append(StationXCableType(station_type, cable_type))
    sxc_maxi = max(lll, key=lambda sxc: sxc.rating)

    dic_station_y = {station.y: station.id for station in instance.substation_locations}
    dic_turbine_y = defaultdict(list)
    for turbine in instance.wind_turbines:
        dic_turbine_y[turbine.y].append(turbine.id)

    turb_to_stat = {}
    for y in dic_turbine_y:
        _, ys_min = min((abs(y-ys),ys) for ys in dic_station_y)
        turb_to_stat[y] = ys_min

    substation_type = sxc_maxi.station_type.id
    to_mainland_cable_type = sxc_maxi.cable_type.id
    substations = [Substation(dic_station_y[yy], to_mainland_cable_type, substation_type) for yy in set(turb_to_stat.values())]

    turbines = [Turbine(wind_turbine.id, dic_station_y[turb_to_stat[wind_turbine.y]]) for wind_turbine in instance.wind_turbines]

    ss_cable_type = max(instance.substation_substation_cable_types, key=lambda cable:cable.probability_of_failure).id

    l_station_y = [ for in dic_station_y.items()]

    sol = Solution(turbines,substations, [])

    return sol
