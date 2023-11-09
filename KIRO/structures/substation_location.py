from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class SubstationLocation(ById): 
    id      :   int
    x       :   float
    y       :   float