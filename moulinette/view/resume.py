"""Default, empty instance visualization tool."""

# import matplotlib.pyplot as plt
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
    l_pas_liste = []
    for arg, code in IMPORT_DICT.items():
        val = instance.__getattribute__(arg)
        if isinstance(val, list):
            print(f"{code: <20} : {len(val): >4} éléments")
        else:
            l_pas_liste.append((code, val))
    for code, val in l_pas_liste:
        print(f"{code: <20} : {val}")
    # print(WindTurbine.by_id(1))
