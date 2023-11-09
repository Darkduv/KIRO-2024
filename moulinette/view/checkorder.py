"""Default, empty instance visualization tool."""

# import matplotlib.pyplot as plt
from model import *

def view(instance: Instance):
    """Do nothing."""
    ok = True
    for job in instance.jobs:
        seq = job.sequence[:]
        seq.sort()
        if seq != job.sequence:
            ok = False
            break
    if not ok:
        print(job)
        print(seq)
    print("task sorted = ", ok)
    for task in instance.tasks:
        if task.processing_time == 0:
            print("task processing time = 0")
    # todo: implement
