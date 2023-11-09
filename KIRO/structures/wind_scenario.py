from dataclasses import dataclass

@dataclass
class WindScenario : 
    power_generation    : float
    probability         : float
    id                  : int 