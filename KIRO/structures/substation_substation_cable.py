from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class SubstationSubstationCable(ById):
    substation_id       : int
    other_substation_id : int
    cable_type          : int