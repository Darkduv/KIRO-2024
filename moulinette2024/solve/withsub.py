"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar

from collections import defaultdict


@chrono
def solve(instance: Instance):
    """Rejoint chaque substation "extérieure" sur la prochaine plus au centre"""
    lll = []
    for station_type in instance.substation_types:
        for cable_type in instance.land_substation_cable_types:
            lll.append(StationXCableType(station_type, cable_type))
    # sxc_maxi = max(lll, key=lambda sxc: (sxc.rating, -sxc.fixed_cost, -sxc.variable_cost))
    sxc_maxi = max(lll, key=lambda sxc: (sxc.rating, -sxc.variable_cost, -sxc.fixed_cost))

    locations = sorted(instance.substation_locations, key=lambda loc: -loc.x)
    dic_station_y = {station.y: station.id for station in locations}
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

    ss_cable_type = min(instance.substation_substation_cable_types, key=lambda cable:cable.rating).id

    l_station_y = [(yy, s_id) for yy, s_id in dic_station_y.items()]

    l_station_y.sort()
    inter_stat = []
    for i, (yy, s_id) in enumerate(l_station_y[:len(l_station_y)//2]):
        inter_stat.append((s_id, l_station_y[i+1][1]))
    for j, (yy, s_id) in enumerate(l_station_y[::-1][:len(l_station_y)//2-1]):
        inter_stat.append((s_id, l_station_y[::-1][j+1][1]))

    inter_stat = [SubstationSubstationCable(s1, s2, ss_cable_type) for s1, s2 in inter_stat]

    sol = Solution(turbines,substations, inter_stat)

    return sol
