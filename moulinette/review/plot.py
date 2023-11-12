"""Review method placeholder."""

import matplotlib.pyplot as plt
from model import *


def review(instance: Instance, solution: Solution):
    """Do nothing."""
    ## TODO TODO vue par défaut
    l0_x = [instance.general_parameters.x]
    l0_y = [instance.general_parameters.y]
    l0_id = ["00"]

    l1_x = [turbine.x for turbine in instance.wind_turbines]
    l1_y = [turbine.y for turbine in instance.wind_turbines]
    l1_id = [str(turbine.id) for turbine in instance.wind_turbines]

    l2_x = [station.x for station in instance.substation_locations]
    l2_y = [station.y for station in instance.substation_locations]
    l2_id = [station.id for station in instance.substation_locations]

    fig, ax = plt.subplots()

    ax.scatter(l0_x, l0_y)
    ax.scatter(l1_x, l1_y)
    ax.scatter(l2_x, l2_y)

    # for x, y, txt in zip(l1_x, l1_y, l1_id):
    #     ax.annotate(txt, (x, y))

    # for x, y, txt in zip(l2_x, l2_y, l2_id):
    #     ax.annotate(txt, (x, y))

    for station in solution.substations:
        location = SubstationLocation.by_id(station.id)
        plt.plot(
            (instance.general_parameters.x,location.x),
                (instance.general_parameters.y, location.y), color="black"
        )

    for turbine in solution.turbines:
        windturb = WindTurbine.by_id(turbine.id)
        station = SubstationLocation.by_id(turbine.substation_id)
        plt.plot(
            (windturb.x,station.x),
                (windturb.y, station.y),
            color='blue'
        )
    for cable in solution.substation_substation_cables:
        s1 = SubstationLocation.by_id(cable.substation_id)
        s2 = SubstationLocation.by_id(cable.other_substation_id)
        plt.arrow(s1.x, s1.y, s2.x-s1.x, s2.y-s1.y, color='green')
    plt.show()
