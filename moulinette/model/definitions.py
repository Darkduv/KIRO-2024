import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type, Generic, TypeVar, Callable, Any, Self
T = TypeVar("T")

import json

# from KIRO.utils import getLogger
# LOGGER=getLogger('EXPORT')
###############################################################################

##################### DICTIONNAIRE POUR EXPORT ################################
EXPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : ('ATTR1', 'ATTR2', 'ATTR3', ...)
    'Template': ('attr1', 'attr2', 'attr3'),
    'Template2': ('attr1', 'attr2'),
}


###############################################################################

########################## FONCTIONS UTILES ###################################
def to_dict(
        un_objet: object,
        export_dict: dict = EXPORT_DICT,
) -> dict:
    """Renvoie un dictionnaire qui contient les attributs demandés à être
    exportés dans export_dict.

    Si les types sont les types 'classiques', la fonction se comporte comme
    l'identité.
    """

    # Si type de base, on renvoie un_objet
    if isinstance(un_objet, (int, float, str, type(None))):
        return un_objet

    # Si c'est un itérable, on applique la fonction à chaque élément de la
    # liste
    elif isinstance(un_objet, (list, tuple)):
        return [to_dict(element) for element in un_objet]

    # Si c'est un dictionnaire, on applique la fonction sur la value
    elif isinstance(un_objet, (dict,)):
        return {
            key: to_dict(value)
            for key, value in un_objet.items()
        }

    # Dans les cas où on doit faire l'opération sur un objet plus complexe
    else:

        # On récupère les attributs à exporter, à partir du nom de la classe
        attributs_classe = export_dict.get(un_objet.__class__.__name__, None)

        # Si jamais le nom de la classe est dans le dictionanire
        if attributs_classe:

            # On renvoie les attributs que le dictionnaire marque comme étant
            #   à exporter
            return {
                attr: to_dict(getattr(un_objet, attr, None))
                for attr in attributs_classe
            }

        # Sinon
        else:
            # On renvoie tout ce qu'il y a dans __dict__ (croisez les doigts !)
            return {
                attr: to_dict(getattr(un_objet, attr, None))
                for attr in un_objet.__dict__
            }


def to_json(
        un_objet: object,
        export_dict: dict = EXPORT_DICT,
        file_dump: 'str' = './objects.json',
) -> None:
    """Ecrit un objet dans un fichier JSON.

    Args:
        un_objet (object): L'objet à écrire
        export_dict (dict, optional): Le dictionanire qui dicte comment les
            classes custom doivent être exportées
        file_dump (str, optional): Le chemin où le json sera écrit.
             Defaults to './objects.json'.
    """
    with open(file_dump, 'w') as f:
        # Some logging
        # LOGGER.info(f"Writing json file : {file_dump}")
        # Passage au format JSON via json.dumps
        #   (on se sert de assemble_json)
        json_write = json.dumps(
            to_dict(un_objet=un_objet, export_dict=export_dict),
            ensure_ascii=False,
            indent=4
        )
        # Ecriture
        f.write(json_write)


##############################




class Container(Generic[T]):

    def __init__(self, type_: Type[T]):
        self.container: dict[int, T] = {}
        self.type_ = type_

    def create(self, *args, **kwargs) -> T:
        instance = self.type_(*args, **kwargs)
        self.container[instance.id_] = instance
        return instance

    def __getitem__(self, item: int):
        return self.container[item]


@dataclass
class Example:
    """bonjour"""
    id_: int


example_container: Container[Example] = Container(Example)
example33 = example_container.create(33)


class ById(ABC):
    dict_id = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.dict_id = {}

    @property
    def id_(self) -> int:
        return self.id


    def __post_init__(self):
        self.dict_id[self.id_] = self

    @classmethod
    def by_id(cls, id_: int):
        try:
            return cls.dict_id[id_]
        except KeyError as e:
            print("KeyError : ", f"cls.__name__ = {cls.__name__}, id = {id_}")
            raise e

###################################

@dataclass
class LandSubstationCableType(ById):
    rating                  : float
    probability_of_failure  : float
    variable_cost           : float
    id                      : int
    fixed_cost              : float


@dataclass
class Parameters:
    fixed_cost_cable        : float
    variable_cost_cable     : float
    curtailing_penalty      : float
    curtailing_cost         : float
    x                       : float
    y                       : float
    maximum_power           : float
    maximum_curtailing      : float



@dataclass
class SubstationLocation(ById) :
    id      :   int
    x       :   float
    y       :   float

@dataclass
class SubstationSubstationCableType(ById):
    rating          : float
    variable_cost   : float
    id              : int
    fixed_cost      : float


@dataclass
class SubstationType(ById) :
    cost                    : float
    rating                  : float
    probability_of_failure  : float
    id                      : int

@dataclass
class WindScenario(ById) :
    power_generation    : float
    probability         : float
    id                  : int

@dataclass
class WindTurbine(ById) :
    id      : int
    x       : float
    y       : float


@dataclass
class Instance:

    land_substation_cable_types: list[LandSubstationCableType]
    wind_turbines: list[WindTurbine]
    wind_scenarios: list[WindScenario]
    substation_locations: list[SubstationLocation]
    substation_types: list[SubstationType]
    general_parameters: Parameters
    substation_substation_cable_types: list[SubstationSubstationCableType]

    def __post_init__(
            self,
    )->None:
        
        self.mainland_coords = (self.general_parameters.x, self.general_parameters.y)
        self.turbines_coords = {
            turbine.id: (turbine.x, turbine.y)
            for turbine in self.wind_turbines
        }

        self.substations_coords = {
            substation.id: (substation.x, substation.y)
            for substation in self.substation_locations
        }

        self.distance_of_turbine_to_substation = {
            turbine: {
                substation: ((tx-sx)**2 + (ty-sy)**2)**0.5
                for substation, (sx, sy) in self.substations_coords.items()
            }
            for turbine, (tx, ty) in self.turbines_coords.items()
        }

        self.distance_of_substation_to_turbine = {
            substation: {
                turbine: self.distance_of_turbine_to_substation[turbine][substation]
                for turbine in self.turbines_coords.keys()
            }
            for substation in self.substations_coords.keys()
        }

        self.distance_of_substation_to_mainland = {
            substation: ((self.mainland_coords[0]-sx)**2 + (self.mainland_coords[1]-sy)**2)**0.5
            for substation, (sx, sy) in self.substations_coords.items()
        }

        self.distance_of_substation_to_other_substation = {
            substation: {
                other: ((s1x-s2x)**2 + (s1y-s2y)**2)**0.5
                for other, (s2x, s2y) in self.substations_coords.items()
            }
            for substation, (s1x, s1y) in self.substations_coords.items()
        }


#######

@dataclass
class Turbine :
    id              : int
    substation_id   : int

@dataclass
class SubstationSubstationCable :
    substation_id       : int
    other_substation_id : int
    cable_type          : int

@dataclass
class Substation(ById):
    id              : int
    land_cable_type : int
    substation_type : int


EXPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : ('ATTR1', 'ATTR2', 'ATTR3', ...)
    'Substation': ('id', 'land_cable_type', 'substation_type'),
    'Turbine': ('id', 'substation_id'),
    'SubstationSubstationCable': (
    'substation_id', 'other_substation_id', 'cable_type'),
}

##################### DICTIONNAIRE POUR EXPORT ################################
IMPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : Classe correspondante
    'land_substation_cable_types': LandSubstationCableType,
    'wind_turbines': WindTurbine,
    'wind_scenarios': WindScenario,
    'substation_locations': SubstationLocation,
    'substation_types': SubstationType,
    'general_parameters': Parameters,
    'substation_substation_cable_types': SubstationSubstationCableType,
    'substations': Substation,
    'substation_substation_cables': SubstationSubstationCable,
    'turbines': Turbine,
}


###############################################################################

########################## FONCTIONS UTILES ###################################


@dataclass
class Solution:
    turbines: list[Turbine]
    substations: list[Substation]
    substation_substation_cables: list[SubstationSubstationCable]

    def add_turbine(self, turb: Turbine):
        self.turbines.append(turb)

    def add_substation(self, substa: Substation):
        self.substations.append(substa)

    def add_sub_sub_cable(self, sub_sub_cable: SubstationSubstationCable):
        self.substation_substation_cables.append(sub_sub_cable)

    def assemble_dict(self, ) -> dict:
        result = {
            'substations': [to_dict(e) for e in self.substations],
            'turbines': [to_dict(e) for e in self.turbines],
            'substation_substation_cables': [to_dict(e) for e in
                                             self.substation_substation_cables],
        }
        return result

    def to_json(self, json_file: str):
        to_json(
            self.assemble_dict(),
            export_dict=EXPORT_DICT,
            file_dump=json_file,
        )

    @classmethod
    def from_json(cls, json_dict) -> Self:
        import_dict = IMPORT_DICT
        # on sort un dico

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

        return Solution(**result)

@dataclass
class StationXCableType(ById):

    def __init__(self, station_type: SubstationType, cable_type: LandSubstationCableType):
        self.station_type = station_type
        self.cable_type = cable_type
        self.fixed_cost = station_type.cost + cable_type.fixed_cost
        self.variable_cost = cable_type.variable_cost
        self.id = station_type.id*1000+cable_type.id
        self.probability_of_failure = station_type.probability_of_failure + cable_type.probability_of_failure

        self.rating = min(station_type.rating, cable_type.rating)


###############################################################################
