from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class LandSubstationCableType(ById):
    rating                  : float
    probability_of_failure  : float
    variable_cost           : float
    id                      : int
    fixed_cost              : float