"""Default, empty instance visualization tool."""

# import matplotlib.pyplot as plt
from model import *

IMPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : Classe correspondante
    'land_substation_cable_types'           : LandSubstationCableType,
    'wind_turbines'                         : WindTurbine,
    'wind_scenarios'                        : WindScenario,
    'substation_locations'                  : SubstationLocation,
    'substation_types'                      : SubstationType,
    'general_parameters'                    : Parameters,
    'substation_substation_cable_types'     : SubstationSubstationCableType,
}


def view(instance: Instance):
    """Do nothing."""
    ## TODO TODO vue par défaut
    for arg in IMPORT_DICT:
        print(f"#########################  {arg}   ###############")
        val = instance.__getattribute__(arg)
        if isinstance(val, list):
            for i, el in enumerate(val):
                print(f"{i: >10} :  {el}")
        else:
            print(val)
    print(WindTurbine.by_id(1))
