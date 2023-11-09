from KIRO.structures import Turbine, Substation, SubstationSubstationCable

from KIRO.export import to_dict, to_json

from dataclasses import dataclass

EXPORT_DICT = {
    # 'NOM_DE_LA_CLASSE' : ('ATTR1', 'ATTR2', 'ATTR3', ...)
    'Substation' : ('id', 'land_cable_type', 'substation_type'),
    'Turbine' : ('id', 'substation_id'),
    'SubstationSubstationCable' : ('substation_id', 'other_substation_id', 'cable_type'),
}

@dataclass
class InstanceExporter :
    turbines                    :list[Turbine]
    substations                 :list[Substation]
    substation_substation_cables:list[SubstationSubstationCable]

    def add_turbine(self, turb:Turbine):
        self.turbines.append(turb)
    
    def add_substation(self, substa:Substation):
        self.substations.append(substa)
    
    def add_sub_sub_cable(self, sub_sub_cable:SubstationSubstationCable):
        self.substation_substation_cables.append(sub_sub_cable)

    def assemble_dict(self, )->dict:
        result = {
            'substations' : [to_dict(e) for e in self.substations],
            'turbines' : [to_dict(e) for e in self.turbines],
            'substation_substation_cables' : [to_dict(e) for e in self.substation_substation_cables],
        }
    
    def to_json(self, json_file:str):
        to_json(
            self.assemble_dict(),
            export_dict=EXPORT_DICT,
            file_dump=json_file,
        )
