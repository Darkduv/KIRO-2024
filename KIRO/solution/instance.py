
@dataclass
class Instance:
    land_substation_cable_types: list[LandSubstationCableType]
    wind_turbines: list[WindTurbine]
    wind_scenarios: list[WindScenario]
    substation_locations: list[SubstationLocation]
    substation_types: list[SubstationType]
    general_parameters: Parameters
    substation_substation_cable_types: list[SubstationSubstationCableType]
