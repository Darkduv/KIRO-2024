from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class WindScenario(ById): 
    power_generation    : float
    probability         : float
    id                  : int 