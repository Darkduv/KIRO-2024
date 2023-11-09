"""System arguments parser."""

import re
import sys
from dataclasses import dataclass
from functools import partial
from typing import List

import data

from .service import Service


@dataclass
class Options:
    """Solver options parsed from system arguments."""

    service: Service
    aliases: List[str]


def parse():
    """Parse system arguments to get source package and instance aliases.
    Service name will default to 'solve'.
    Default service source is defined in Service class arguments.
    alias list will default to all instances.
    """
    args = sys.argv

    name = "solve"
    flags = list(filter(partial(re.fullmatch, "--.*"), args))
    for flag in flags:
        args.remove(flag)
        name = re.sub(r"\W", "", flag)

    service = Service.load(name)

    try:
        source, *aliases = args[1:]
        source = re.sub(r"\W", "", source)
    except ValueError:
        source, aliases = None, []

    if not aliases:
        aliases = list(set(data.Driver.registry.values()))
    aliases.sort()
    return Options(service(source), aliases)
