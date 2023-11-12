"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar

from collections import defaultdict
from random import choice


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
    dic_station_y2 = defaultdict(list)
    for station in instance.substation_locations:
        dic_station_y2[station.y].append(station.id)

    turb_to_stat = {}
    for y in dic_turbine_y:
        _, ys_min = min((abs(y-ys),ys) for ys in dic_station_y)
        turb_to_stat[y] = ys_min

    substation_type = sxc_maxi.station_type.id
    to_mainland_cable_type = sxc_maxi.cable_type.id
    substations = [Substation(dic_station_y[yy], to_mainland_cable_type, substation_type) for yy in set(turb_to_stat.values())]

    turbines = [Turbine(wind_turbine.id, dic_station_y[turb_to_stat[wind_turbine.y]]) for wind_turbine in instance.wind_turbines]

    ss_cable_type = min(instance.substation_substation_cable_types, key=lambda cable:cable.rating).id


    inter_stat = []
    for yy, s_id in dic_station_y.items():
        stat2 = choice([a for a in dic_station_y2[yy] if a != s_id])
        inter_stat.append((s_id, stat2))
        substations.append(Substation(stat2, to_mainland_cable_type, substation_type))

    inter_stat = [SubstationSubstationCable(s1, s2, ss_cable_type) for s1, s2 in inter_stat]

    sol = Solution(turbines,substations, inter_stat)

    return sol
