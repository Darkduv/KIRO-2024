"""Default, empty instance visualization tool."""

# import matplotlib.pyplot as plt
from model import *

def view(instance: Instance):
    """Do nothing."""
    print(instance.parameters.size)
    print(instance.parameters.costs)
