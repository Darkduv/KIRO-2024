"""Instance visualization service."""

from control import Service

from .default import view


class View(Service, name=__name__):
    """Nothing specific for this service, just load the 'view' function."""
