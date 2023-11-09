############################# IMPORTS #########################################
import json
from typing import Any


# from KIRO.utils import getLogger
# LOGGER=getLogger('IMPORT')

from KIRO.structures import (
    LandSubstationCableType,
    WindTurbine,
    WindScenario,
    SubstationLocation,
    SubstationType,
    Parameters,
    SubstationSubstationCableType,
)

###############################################################################

##################### DICTIONNAIRE POUR EXPORT ################################
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
###############################################################################

########################## FONCTIONS UTILES ###################################
def from_json(
    json_file : str,
    import_dict : dict[str, type]=IMPORT_DICT,
)->dict[str, Any]:
    # on sort un dico
    with open(json_file, 'r') as the_json :
        json_dict = json.loads(the_json.read())
    
    # on parcourt le json et on crée les objets
    result = {}
    for key_json, value in json_dict.items():
        if not isinstance(value, (list, tuple)):
            the_class = import_dict[key_json]
            if 'main_land_station' in value : 
                value['x']=value['main_land_station']['x']
                value['y']=value['main_land_station']['y']
                value.pop('main_land_station')
            result[key_json]=the_class(**value)
        else:
            the_class = import_dict[key_json]
            result[key_json] = []
            for object in value : 
                result[the_class.__name__].append(
                    the_class(**object)
                )

    return result
