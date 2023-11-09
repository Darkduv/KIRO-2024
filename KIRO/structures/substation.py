from dataclasses import dataclass

@dataclass
class Substation :
    id              : int 
    land_cable_type : int
    substation_type : int