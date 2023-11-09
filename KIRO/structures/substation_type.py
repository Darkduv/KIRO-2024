from dataclasses import dataclass

@dataclass
class SubstationType :
    cost                    : float
    rating                  : float
    probability_of_failure  : float
    id                      : int