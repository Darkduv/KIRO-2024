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
    for yy in dic_station_y:
        dic_station_y[yy] = choice(dic_station_y2[yy])
    for yy in dic_station_y2:
        dic_station_y2[yy] = choice([a for a in dic_station_y2[yy] if a != dic_station_y[yy]])

    turb_to_stat = {}
    for y in list(dic_turbine_y)[:len(dic_turbine_y)//2]:
        _, ys_min = min((abs(y-ys),ys) for ys in dic_station_y)
        turb_to_stat[y] = ys_min
    for y in list(dic_turbine_y)[len(dic_turbine_y)//2:]:
        _, ys_min = min((abs(y-ys),ys) for ys in dic_station_y2)
        turb_to_stat[y] = ys_min

    substation_type = sxc_maxi.station_type.id
    to_mainland_cable_type = sxc_maxi.cable_type.id
    substations = [Substation(dic_station_y[yy], to_mainland_cable_type, substation_type) for yy in set(turb_to_stat.values())]

    turbines = [Turbine(wind_turbine.id, dic_station_y[turb_to_stat[wind_turbine.y]]) for wind_turbine in instance.wind_turbines]

    sol = Solution(turbines,substations, [])

    return sol
