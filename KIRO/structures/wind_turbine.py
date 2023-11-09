from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class WindTurbine(ById):
    id      : int
    x       : float
    y       : float