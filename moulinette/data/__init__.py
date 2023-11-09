"""Handling of input/output files through aliases.
Parsing method to read an Instance and write/retrieve a Solution.
Driver instantiated for one instance by alias.
Parser (loaded with `Driver.load`) implements 'next' iterative parsing method.
"""

from model import *

from .driver import DriverBase
import json
from typing import Any
# todo: download input files

# todo-dev: single output file description


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



class Driver(DriverBase):
    """Custom model building methods."""

    def read(self) -> Instance:
        # TODO TODO lecture de l'instance
        """Read instance from file."""
        import_dict = IMPORT_DICT
        reader = self.load("r", "in")
        json_dict = reader.next()
        # on parcourt le json et on crée les objets
        result = {}
        for key_json, value in json_dict.items():
            if not isinstance(value, (list, tuple)):
                the_class = import_dict[key_json]
                if 'main_land_station' in value:
                    value['x'] = value['main_land_station']['x']
                    value['y'] = value['main_land_station']['y']
                    value.pop('main_land_station')
                result[key_json] = the_class(**value)
            else:
                the_class = import_dict[key_json]
                result[key_json] = []
                for object in value:
                    result[key_json].append(
                        the_class(**object)
                    )
        # print(result)
        return Instance(**result)

    def write(self, solution):
        """Write solution to file."""
        # TODO TODO écriture du résultat
        writer = self.load("w", "out")
        dico = solution.assemble_dict()
        print(dico)
        writer.next(solution.assemble_dict())

    def retrieve(self):
        """Read solution from file."""
        # TODO TODO lecture du résultat
        reader = self.load("r", "out")
        json_sol = reader.next()
        return Solution.from_json(json_sol)


def better_gain(gain):
    """Is the gain better ?
    # TODO TODO à vérifier

    if the objective is a minimization, the gains are better if < 0.
    else when gain > 0 :
        correct the return below in function of that."""
    # return gain < 0
    return -1


