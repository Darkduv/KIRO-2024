import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Type, Generic, TypeVar, Callable, Any, Self
T = TypeVar("T")

import json
from collections import defaultdict

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

class ShopType(Enum):
    BODY = "body"
    PAINT = "paint"
    ASSEMBLY = "assembly"

class VehicleType(Enum):
    REGULAR = "regular"
    TWOTONE = "two-tone"

@dataclass
class Shop:
    name:ShopType
    resequencing_lag:int

@dataclass
class Parameter:
    two_tone_delta:int
    resequencing_cost:float

@dataclass
class Vehicle:
    id:int
    type:VehicleType

@dataclass
class Constraint:
    id:int
    shop:ShopType
    cost:float

@dataclass
class BatchSizeConstraint(Constraint):
    min_vehicles:int
    max_vehicles:int
    vehicles:list[int]

@dataclass
class LotChangeConstraint(Constraint):
    partition:list[list[int]]

@dataclass
class RollingWindowConstraint(Constraint):
    window_size:int
    max_vehicles:int
    vehicles:list[int]