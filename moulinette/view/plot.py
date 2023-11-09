"""Default, empty instance visualization tool."""

import matplotlib.pyplot as plt
from model import *

IMPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : Classe correspondante
    'land_substation_cable_types'           : "Q0",
    'wind_turbines'                         : "Turbines",
    'wind_scenarios'                        : "Scenarios",
    'substation_locations'                  : "LieuStation",
    'substation_types'                      : "S_types",
    'general_parameters'                    : "Param",
    'substation_substation_cable_types'     : "QS",
}


def view(instance: Instance):
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

    for x, y, txt in zip(l1_x, l1_y, l1_id):
        ax.annotate(txt, (x, y))

    plt.show()
