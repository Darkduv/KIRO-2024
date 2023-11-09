from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class SubstationType(ById):
    cost                    : float
    rating                  : float
    probability_of_failure  : float
    id                      : int