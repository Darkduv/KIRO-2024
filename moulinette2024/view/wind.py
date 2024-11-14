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
    # for scenario in instance.wind_scenarios:
    #     print(f"id={scenario.id: >4} ; power_generation =")

    l_power = [scenario.power_generation for scenario in instance.wind_scenarios]
    l_proba = [scenario.probability for scenario in instance.wind_scenarios]
    l_id = [scenario.id for scenario in instance.wind_scenarios]

    fig, ax = plt.subplots()

    ax.scatter(l_power, l_proba)

    for x, y, txt in zip(l_power, l_proba, l_id):
        ax.annotate(txt, (x, y))


    plt.show()
