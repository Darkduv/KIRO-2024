"""Solution scoring and verification."""

# import numpy as np
from .definitions import *


def score(
    instance : Instance, 
    solution : Solution,         
)->float:
    
    # Cout de construction des substations en fonction de leur type
    construction_cost_1 = sum(
        [
            solution.substations_types[substation.id].cost
            for substation in solution.substations
        ]
    )
    
    # Cout de construction des câbles vers le mainland
    construction_cost_2 = 0
    for substation in solution.substations:
        ml_cable_type = solution.mainland_cable_types[substation.id]
        (sx, sy) = solution.substations_locations[substation.id]
        dx = (sx- instance.general_parameters.x)
        dy = (sy - instance.general_parameters.y)
        longueur = (dx**2 + dy**2)**0.5
        construction_cost_2 += ml_cable_type.fixed_cost + longueur*ml_cable_type.variable_cost
    
    # Cout de construction des câbles entre les substations
    construction_cost_3 = 0
    for subcable in solution.substation_substation_cables:
        type_cable=solution.substation_substation_cables_types[subcable.substation_id]
        (s1x, s1y)=solution.substations_locations[subcable.substation_id]
        (s2x, s2y)=solution.substations_locations[subcable.other_substation_id]
        dx=(s1x-s2x)
        dy=(s1y-s2y)
        longueur = (dx**2 + dy**2)**0.5
        construction_cost_3 += type_cable.fixed_cost + longueur*type_cable.variable_cost
    
    # Cout de construction des câbles entre les turbines et les sub
    construction_cost_4 = 0
    for turbine in solution.turbines:
        (tx, ty)=solution.turbines_locations[turbine.id]
        (sx, sy)=solution.substations_locations[turbine.substation_id]
        dx=(sx-tx)
        dy=(sy-ty)
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
            proba_fail_1=solution.substations_types[substation.id].probability_of_failure
            proba_fail_2=solution.mainland_cable_types[substation.id].probability_of_failure
            proba_fail = proba_fail_1+proba_fail_2

            c0=instance.general_parameters.curtailing_cost
            cp=instance.general_parameters.curtailing_penalty
            cmax=instance.general_parameters.maximum_curtailing

            def cost_from_curtailing(curtainling:float):
                return c0*curtainling+cp*max(0, curtainling-cmax)
            
            #### Calcul de cn
            c_n = 0
            for other_substa in solution.substations :

                nb_turbs=len(solution.turbines_connected_to_substations[other_substa.id])
                rate=solution.substations_types[other_substa.id].rating 
                rate_c=solution.mainland_cable_types[other_substa.id].rating
                c_n += max(0, power*nb_turbs-min(rate, rate_c))
            
            #### Calcul de cf
            c_f = 0
            nb_turbs_current=len(solution.turbines_connected_to_substations[substation.id])

            cable_vers_other=solution.exiting_cables[substation.id]

            if len(cable_vers_other) >0 : 
                cable_vers_other = cable_vers_other[0]

                rate1=solution.substation_substation_cables_types[substation.id].rating
                other_substa_id = cable_vers_other.other_substation_id
                type_other=solution.substations_types[other_substa_id]
                cableotehr=solution.mainland_cable_types[other_substa_id]
                nb_turbines_other=len(solution.turbines_connected_to_substations[other_substa_id])
                otherterm2=min(rate1, power*nb_turbs_current)
                otherterm3=min(type_other.rating, cableotehr.rating)
                otherterm = max(0,power*nb_turbines_other+otherterm2-otherterm3)

                c_f += otherterm

            else:
                rate1=0
        
            c_f += max(0, power*nb_turbs_current-rate1)

            sous_cout += proba_fail*cost_from_curtailing(c_f) + (1-proba_fail)*cost_from_curtailing(c_n)
        
        cout_operationnel += proba*sous_cout
    
    return construction_cost_1\
            + construction_cost_2\
            + construction_cost_3\
            + construction_cost_4\
            + cout_operationnel

