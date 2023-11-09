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
    SubstationSubstationCable,
    Substation,
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
    
    # Cout opérationnel
    cout_operationnel = 0
    for scenario in instance.wind_scenarios:
        proba = scenario.probability
        power = scenario.power_generation
        sous_cout = 0
        for substation in solution.substations :
            type_station = substation.substation_type
            le_type:SubstationType= SubstationType.by_id(type_station)
            proba_fail_1 = le_type.probability_of_failure

            type_mainland_cable = substation.land_cable_type
            le_type:LandSubstationCableType = LandSubstationCableType.by_id(type_mainland_cable)
            proba_fail_2 = le_type.probability_of_failure

            proba_fail = proba_fail_1+proba_fail_2

            c0=instance.general_parameters.curtailing_cost
            cp=instance.general_parameters.curtailing_penalty
            cmax=instance.general_parameters.maximum_curtailing

            def cost_from_curtailing(curtainling:float):
                return c0*curtainling+cp*max(0, curtainling-cmax)
            
            c_n = 0

            for other_substa in solution.substations :

                turbines_connected = [
                    turbine
                    for turbine in solution.turbines
                    if turbine.substation_id == other_substa.id
                ]

                type_sub:SubstationType = SubstationType.by_id(other_substa.substation_type)
                rate = type_sub.rating

                type_cable:LandSubstationCableType=LandSubstationCableType.by_id(other_substa.land_cable_type)
                rate_c = type_cable.rating

                c_n += max(0, power*len(turbines_connected)-min(rate, rate_c))
            
            c_f = 0

            turbines_connected = [
                    turbine
                    for turbine in solution.turbines
                    if turbine.substation_id == substation.id
            ]

            

            cable_vers_other:SubstationSubstationCable = [
                cable 
                for cable in solution.substation_substation_cables
                if cable.substation_id == substation.id
            ]
            if len(cable_vers_other) >0 : 
                cable_vers_other = cable_vers_other[0]
                type_cable_vers_other = cable_vers_other.cable_type

                type_cable_vers_other :SubstationSubstationCableType= SubstationSubstationCableType.by_id(type_cable_vers_other)
                rate1 = type_cable_vers_other.rating


                other_substa:Substation = Substation.by_id(cable_vers_other.other_substation_id)
                type_other:SubstationType = SubstationType.by_id(other_substa.substation_type)
                cableotehr:LandSubstationCableType = LandSubstationCableType.by_id(other_substa.land_cable_type)

                turbines_connected_other = [
                    turbine
                    for turbine in solution.turbines
                    if turbine.substation_id == other_substa.id
                ]

                otherterm2=min(rate1, power*len(turbines_connected))


                otherterm3=min(type_other.rating, cableotehr.rating)

                otherterm = max(0,power*len(turbines_connected_other)+otherterm2-otherterm3)

                c_f += otherterm

            else:
                rate1=0
        
            
            c_f += max(0, power*len(turbines_connected)-rate1)


            sous_cout += proba_fail*cost_from_curtailing(c_f) + (1-proba_fail)*cost_from_curtailing(c_n)
        
        cout_operationnel += proba*sous_cout
    
    return construction_cost_1\
            + construction_cost_2\
            + construction_cost_3\
            + construction_cost_4\
            + cout_operationnel
