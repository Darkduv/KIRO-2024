from dataclasses import dataclass

@dataclass
class LandSubstationCableType:
    rating                  : float
    probability_of_failure  : float
    variable_cost           : float
    id                      : int
    fixed_cost              : float