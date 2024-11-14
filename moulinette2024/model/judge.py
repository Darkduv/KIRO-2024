"""Solution scoring and verification."""

# import numpy as np
from .definitions import *


def reseq_2tones(sigma: list[int], two_tones: list[int], delta: int) -> list[int]:
    sigma = sigma[:]
    two_tones = set(two_tones)
    i = 0
    while i < len(sigma):
        v = sigma[i]
        if v not in two_tones:
            i += 1
            continue
        two_tones.remove(v)
        sigma[i:i+delta+1] = sigma[i+1:i+delta+1]+sigma[i:i+1]
    return sigma
def score(
    instance : Instance,
    solution : Solution,
)->float:

