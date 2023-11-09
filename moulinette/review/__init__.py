"""Solution review service."""

from control import Service
from data import Driver


class Review(Service, name=__name__):
    """Render solution data for reviewing."""

    def __call__(self, alias):
        driver = Driver(alias)
        instance = driver.read()
        solution = driver.retrieve()
        return self.call(instance, solution)
