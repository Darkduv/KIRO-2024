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
    @abstractmethod
    def id_(self) -> int:
        ...

    def __post_init__(self):
        self.dict_id[self.id_] = self

    @classmethod
    def by_id(cls, id_: int):
        try:
            return cls.dict_id[id_]
        except KeyError as e:
            print("KeyError : ", f"cls.__name__ = {cls.__name__}, id = {id_}")
            raise e

# @dataclass
# class Instance:
#     """Contains instance data."""
#
# @dataclass
# class Solution:
#     """Contains solution data."""
