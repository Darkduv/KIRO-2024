"""Handling of input/output files through aliases.
Parsing method to read an Instance and write/retrieve a Solution.
Driver instantiated for one instance by alias.
Parser (loaded with `Driver.load`) implements 'next' iterative parsing method.
"""

from model import (
    VehicleType,
    Shop, 
    Parameters, 
    Vehicle, 
    Constraint, 
    BatchSizeConstraint, 
    LotChangeConstraint,
    RollingWindowConstraint,
    Instance, 
    Solution
)

from .driver import DriverBase
import json
from typing import Any
# todo: download input files

# todo-dev: single output file description


###############################################################################

##################### DICTIONNAIRE POUR EXPORT ################################

def read_instance(instance_json:dict)->Instance:
    # A partir de la on peut parcourir a la main l'instance
        
        # On fait les shops
        body_data = [e for e in instance_json["shops"] if e["name"] == "body"][0]
        paint_data = [e for e in instance_json["shops"] if e["name"] == "paint"][0]
        assembly_data = [e for e in instance_json["shops"] if e["name"] == "assembly"][0]
        
        bodyshop = Shop(**body_data)
        paintshop = Shop(**paint_data)
        assemblyshop = Shop(**assembly_data)

        # On fait les paramètres
        two_tone_delta = instance_json["parameters"]["two_tone_delta"]
        resequencing_cost = instance_json["parameters"]["resequencing_cost"]

        # On fait les véhicules
        vehicles_data = instance_json["vehicles"]
        vehicles = [
            Vehicle(
                id = v["id"],
                type=VehicleType.get(v["type"]),
            )
            for v in vehicles_data
        ]

        # On fait les contraintes
        cons_data = instance_json["constraints"]
        constraints : list[Constraint]= []
        for c in cons_data :
            c_type = c["type"]
            match c_type:
                case "batch_size":
                    constraints.append(
                        BatchSizeConstraint(**c)
                    )
                case "lot_change":
                    constraints.append(
                        LotChangeConstraint(**c)
                    )
                case "rolling_window":
                    constraints.append(
                        RollingWindowConstraint(**c)
                    )
                case _ :
                    raise ValueError("Erreur dans la lecture du json Constraints")
                
        # print(result)
        return Instance(
            body_shop=bodyshop,
            paint_shop=paintshop,
            assembly_shop=assemblyshop,
            parameters=Parameters(two_tone_delta=two_tone_delta, resequencing_cost=resequencing_cost),
            vehicles=vehicles,
            constraints=constraints,
        )


class Driver(DriverBase):
    """Custom model building methods."""

    def read(self) -> Instance:
        # TODO TODO lecture de l'instance
        """Read instance from file."""
        reader = self.load("r", "in")
        json_dict = reader.next()

        return read_instance(instance_json=json_dict)

    def write(self, solution:Solution):
        """Write solution to file."""
        # TODO TODO écriture du résultat
        writer = self.load("w", "out")
        dico = solution.assemble_dict()
        print(dico)
        writer.next(dico)

    def retrieve(self):
        """Read solution from file."""
        # TODO TODO lecture du résultat
        reader = self.load("r", "out")
        json_sol = reader.next()
        return Solution.from_json(json_sol)


def better_gain(gain):
    """Is the gain better ?
    # TODO TODO à vérifier

    if the objective is a minimization, the gains are better if < 0.
    else when gain > 0 :
        correct the return below in function of that."""
    return gain < 0


