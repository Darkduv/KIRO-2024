from dataclasses import dataclass

from KIRO.utils import ById

@dataclass
class Parameters:
    fixed_cost_cable        : float
    variable_cost_cable     : float
    curtailing_penalty      : float
    curtailing_cost         : float
    x                       : float
    y                       : float
    maximum_power           : float
    maximum_curtailing      : float
