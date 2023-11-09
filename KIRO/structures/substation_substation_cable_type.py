from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class SubstationSubstationCableType(ById):
    rating          : float
    variable_cost   : float
    id              : int
    fixed_cost      : float 