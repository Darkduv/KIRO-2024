import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type, Generic, TypeVar, Callable, Any
T = TypeVar("T")


class Container(Generic[T]):

    def __init__(self, type_: Type[T]):
        self.container: dict[int, T] = {}
        self.type_ = type_

    def create(self, *args, **kwargs) -> T:
        instance = self.type_(*args, **kwargs)
        self.container[instance.id_] = instance
        return instance

    def __getitem__(self, item: int):
        return self.container[item]


@dataclass
class Example:
    """bonjour"""
    id_: int


example_container: Container[Example] = Container(Example)
example33 = example_container.create(33)


class ById(ABC):
    dict_id = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.dict_id = {}

    @property
    def id_(self) -> int:
        return self.id


    def __post_init__(self):
        self.dict_id[self.id_] = self

    @classmethod
    def by_id(cls, id_: int):
        try:
            return cls.dict_id[id_]
        except KeyError as e:
            print("KeyError : ", f"cls.__name__ = {cls.__name__}, id = {id_}")
            raise e

###################################

@dataclass
class LandSubstationCableType(ById):
    rating                  : float
    probability_of_failure  : float
    variable_cost           : float
    id                      : int
    fixed_cost              : float


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



@dataclass
class SubstationLocation(ById) :
    id      :   int
    x       :   float
    y       :   float

@dataclass
class SubstationSubstationCableType(ById):
    rating          : float
    variable_cost   : float
    id              : int
    fixed_cost      : float


@dataclass
class SubstationType(ById) :
    cost                    : float
    rating                  : float
    probability_of_failure  : float
    id                      : int

@dataclass
class WindScenario(ById) :
    power_generation    : float
    probability         : float
    id                  : int

@dataclass
class WindTurbine(ById) :
    id      : int
    x       : float
    y       : float


@dataclass
class Instance:

    land_substation_cable_types: list[LandSubstationCableType]
    wind_turbines: list[WindTurbine]
    wind_scenarios: list[WindScenario]
    substation_locations: list[SubstationLocation]
    substation_types: list[SubstationType]
    general_parameters: Parameters
    substation_substation_cable_types: list[SubstationSubstationCableType]



Solution = dict