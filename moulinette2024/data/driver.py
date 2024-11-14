"""Driver setup for a given alias.
Automated loading of instance aliases.
"""
import os

from .parse import Parser


def aliases(name):
    """Provide all aliases for an instance name."""
    return name.split("_", 1) + [name]  # todo: more aliases


def get_names():
    """Load instance names into alias register.
    Instances are found in 'input/', with file extension '.json'.
    """
    directory = os.path.dirname(__file__)
    all_files = os.listdir(f"{directory}/input")
    instances = [name[:-5] for name in all_files if name.endswith(".json")]
    instances.sort()
    registry = {}
    for name in instances:
        for alias in aliases(name):
            registry[alias] = name
    return registry


class DriverBase:
    """Interact with data files for an instance."""

    registry = get_names()

    def __init__(self, alias):
        name = self.registry[alias]
        directory = os.path.dirname(__file__)
        self.path = f"{directory}/{{ext}}put/{name}.json"

    def name(self, ext):
        """Build file path for given extension."""
        return self.path.format(ext=ext)

    def load(self, mode, ext):
        """Load parser for given mode and file extension."""
        return Parser(self.name(ext), mode)
