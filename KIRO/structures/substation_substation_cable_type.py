from dataclasses import dataclass

@dataclass
class SubstationSubstationCableType:
    rating          : float
    variable_cost   : float
    id              : int
    fixed_cost      : float 