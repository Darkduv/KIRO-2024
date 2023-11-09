from KIRO.inputs.costs import *

from KIRO.solution import (
    Solution, 
    Instance,
)

from KIRO.structures import (
    SubstationType,
    LandSubstationCableType,
    SubstationSubstationCableType,
    SubstationLocation,
    WindTurbine,
)

def judge(
    instance : Instance, 
    solution : Solution,         
)->float:
    
    # Cout de construction des substations en fonction de leur type
    construction_cost_1 = 0
    for substation in solution.substations:
        type_station = substation.substation_type
        le_type:SubstationType= SubstationType.by_id(type_station)
        construction_cost_1 += le_type.cost
    
    # Cout de construction des câbles vers le mainland
    construction_cost_2 = 0
    for substation in solution.substations:
        type_mainland_cable = substation.land_cable_type
        le_type:LandSubstationCableType = LandSubstationCableType.by_id(type_mainland_cable)

        location_substation:SubstationLocation = SubstationLocation.by_id(substation.id)
        dx = (location_substation.x - instance.general_parameters.x)
        dy = (location_substation.y - instance.general_parameters.y)
        longueur = (dx**2 + dy**2)**0.5

        construction_cost_2 += le_type.fixed_cost + longueur*le_type.variable_cost
    
    # Cout de construction des câbles entre les substations
    construction_cost_3 = 0
    for subcable in solution.substation_substation_cables:
        type_cable = subcable.cable_type
        le_type:SubstationSubstationCableType = SubstationSubstationCableType.by_id(type_cable)
        
        location_substation:SubstationLocation = SubstationLocation.by_id(subcable.substation_id)
        location_other:SubstationLocation = SubstationLocation.by_id(subcable.other_substation_id)
        dx = (location_substation.x - location_other.x)
        dy = (location_substation.y - location_other.y)
        longueur = (dx**2 + dy**2)**0.5

        construction_cost_3 += le_type.fixed_cost + longueur*le_type.variable_cost
    
    # Cout de construction des câbles entre les turbines et les sub
    construction_cost_4 = 0
    for turbine in solution.turbines:
        location_turbine :WindTurbine= WindTurbine.by_id(turbine.id)
        location_sub :SubstationLocation= SubstationLocation.by_id(turbine.substation_id)

        dx = (location_turbine.x-location_sub.x)
        dy = (location_turbine.y-location_sub.y)
        longueur = (dx**2 + dy**2)**0.5

        construction_cost_4 += instance.general_parameters.fixed_cost_cable \
                                + longueur*instance.general_parameters.variable_cost_cable
    

    return construction_cost_1\
            + construction_cost_2\
            + construction_cost_3
