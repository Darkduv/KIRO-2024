"""Default, empty instance visualization tool."""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

    l_proba = [s_to_c.probability_of_failure for s_to_c in instance.land_substation_cable_types]
    l_rating = [s_to_c.rating for s_to_c in instance.land_substation_cable_types]
    l_cost = [s_to_c.fixed_cost for s_to_c in instance.land_substation_cable_types]
    l_var_cost = [s_to_c.variable_cost for s_to_c in instance.land_substation_cable_types]
    l_id = [s_to_c.id for s_to_c in instance.land_substation_cable_types]

    vals = [
        ("proba", l_proba),
        ("rating", l_rating),
        ("cost", l_cost),
        ("var_cost", l_var_cost),
    ]

    plots_configs = [
        # n° in plot , l_x, l_y, l_z
        (1, 0, 1, 2),
        (2, 0, 1, 3),
        (3, 0, 2, 3),
        (4, 1, 2, 3),
    ]

    fig = plt.figure(figsize=(16,12))

    for num_plot, lx, ly, lz in plots_configs:
        ax1 = fig.add_subplot(220+num_plot, projection='3d')
        ax1.set_xlabel(vals[lx][0])
        ax1.set_ylabel(vals[ly][0])
        ax1.set_zlabel(vals[lz][0])
        ax1.scatter(vals[lx][1], vals[ly][1], vals[lz][1])
        for x, y, z, txt in zip(vals[lx][1], vals[ly][1], vals[lz][1], l_id):
            ax1.text(x, y, z, txt)

    fig.suptitle("Types de Câbles terre <-> Station")
    plt.show()


