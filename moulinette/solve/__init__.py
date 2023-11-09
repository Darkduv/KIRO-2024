"""Compute solution from instance, report gains and upload results."""

from numpy import inf

import model
import tools
from control import Service, upload
from data import Driver, better_gain


class Solve(Service, name=__name__):
    """Solver service."""

    def __init__(self, name):
        super().__init__(name)
        self.solutions = {}
        self.gains = {}

    def __call__(self, alias):
        print(f"Solving instance {alias}")
        driver = Driver(alias)
        instance = driver.read()
        solution = self.call(instance)

        score = model.score(instance, solution)
        try:
            old_score = model.score(instance, driver.retrieve())
        except FileNotFoundError:
            old_score = inf

        if better_gain(delta := score - old_score):
            driver.write(solution)
        self.gains[alias] = score, delta

    def close(self):
        """Prepare upload package and report gains."""
        if upgraded := [
            alias for alias, (score, delta) in self.gains.items()
            if better_gain(delta)
        ]:
            upload(self.path, upgraded)
        message = "{key:<30}: score {value[0]:<10}, gain {value[1]}"
        tools.report("Gains", self.gains, message)
