from moulinette.model.definitions import *
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def simplify_instance(
    instance:Instance,
    nb_senarii_final:int,
)->Instance:
    """Simplifie les scénarios de vent d'une instance pour simplifier les 
    itérations.
    """
    scenarii=instance.wind_scenarios
    powers_and_probabilities=np.array(
        [
            [scenario.power_generation, scenario.probability]
            for scenario in scenarii
        ]
    )
    clusterisation=AgglomerativeClustering(
        n_clusters=nb_senarii_final,
        linkage='single',
    ).fit(powers_and_probabilities)

    new_wind_scenarii = []
    for n_cluster in range(nb_senarii_final):
        labelized_wind=[
            scenario 
            for i, scenario in enumerate(instance.wind_scenarios) 
            if clusterisation.labels_[i]==n_cluster
        ]
        total_probability=sum(
            [
                scenario.probability
                for scenario in labelized_wind
            ]
        )

        mean_probability=total_probability/len(labelized_wind)

        mean_power=sum(
            [
                scenario.power_generation*scenario.probability
                for scenario in labelized_wind
            ]
        )/total_probability

        new_wind_scenarii.append(
            WindScenario(
                power_generation=mean_power,
                probability=mean_probability,
                id=1e6+n_cluster,
            )
        )

    return Instance(
        land_substation_cable_types=instance.land_substation_cable_types,
        wind_turbines=instance.wind_turbines,
        wind_scenarios=new_wind_scenarii,
        substation_locations=instance.substation_locations,
        general_parameters=instance.general_parameters,
        substation_substation_cable_types=instance.substation_substation_cable_types,
        substation_types=instance.substation_types
    )

