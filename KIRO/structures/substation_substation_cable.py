from dataclasses import dataclass

@dataclass
class SubstationSubstationCable :
    substation_id       : int
    other_substation_id : int
    cable_type          : int