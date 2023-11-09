from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class Turbine(ById):
    id              : int
    substation_id   : int