from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class Substation(ById):
    id              : int 
    land_cable_type : int
    substation_type : int