import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type, Generic, TypeVar, Callable, Any
T = TypeVar("T")


@dataclass
class Costs:
    unit_penalty: int  # alpha
    tardiness: int  # beta
    interim: int

    @property
    def alpha(self):
        return self.unit_penalty

    @property
    def beta(self):
        return self.tardiness


@dataclass
class Size:
    nb_jobs: int
    nb_tasks: int
    nb_machines: int
    nb_operators: int


@dataclass
class Parameters:
    """Store the Parameters of an instance"""
    size: Size
    costs: Costs


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


@dataclass
class Job(ById):
    job: int
    sequence: list[int]
    release_date: int
    due_date: int
    weight: int

    @property
    def id_(self):
        return self.job

    @property
    def minimal_time(self):
        return sum(
            Task.by_id(task_id).processing_time
            for task_id in self.sequence
        )

    def minimal_cost(self, costs: Costs):
        c_j = self.minimal_time + self.release_date
        t_j = max(c_j - self.due_date, 0)
        u_j = 1 if t_j > 0 else 0
        return self.weight * (c_j + costs.alpha * u_j + costs.beta * t_j)


@dataclass
class Machine(ById):
    machine: int

    @property
    def id_(self):
        return self.machine
    time_free: int = field(default=0, init=False)


@dataclass
class MachineTask:
    machine: int
    operators: list[int]

    @property
    def time_free(self):
        machine_time_free = Machine.by_id(self.machine).time_free
        op_time_free = min((Operator.by_id(op_id).time_free
                            for op_id in self.operators))
        return max(machine_time_free, op_time_free)


@dataclass
class Task(ById):
    task: int
    processing_time: int
    machines_tasks: list[MachineTask]
    job: int = field(default=None, init=False)
    time_free: int = field(default=0, init=False)

    @property
    def id_(self):
        return self.task

    def min_time_free(self):
        return min(
            (max(mt.time_free, self.time_free) for mt in self.machines_tasks)
        )


@dataclass
class Operator(ById):
    op: int
    time_free: int = field(default=0, init=False)

    @property
    def id_(self):
        return self.op


@dataclass
class Instance:
    """Contains instance data."""
    json_dict: dict
    parameters: Parameters
    jobs: list[Job]
    tasks: list[Task]
    operators: list[Operator]
    machines: list[Machine]


@dataclass
class Schedule:
    task: int
    start: int
    machine: int
    operator: int


@dataclass
class Solution:
    """Contains solution data."""
    schedules: list[Schedule]
