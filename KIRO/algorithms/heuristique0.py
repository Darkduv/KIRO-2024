from KIRO.solution.solution import Solution

from KIRO.structures import (
    Substation, Turbine, SubstationSubstationCable,
)

from KIRO.structures import (
    Turbine, Substation, SubstationSubstationCable,
)

#########

def solve(instance)->Solution:
    return Solution(
        turbines=[Turbine(1, 1)],
        substations=[Substation(1, 1, 1), Substation(2, 1, 1)],
        substation_substation_cables=[SubstationSubstationCable(1, 2, 1)]
    )