from abc import ABC, abstractclassmethod, abstractmethod

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