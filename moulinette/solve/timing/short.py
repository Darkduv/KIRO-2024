import numpy as np

from tools import chrono


@chrono
def better(t1, t2, day):
    pair = [t1, t2]
    switch = [list(fun(pair)) for fun in [list, reversed]]

    scores = []
    for s, t in switch:
        score = t.scores[day]
        if (late := day + t.library.signup) < len(t.scores):
            score += s.scores[late]
        scores.append(score)
    return pair[np.argmax(scores)]


@chrono
def best(times, day):
    timelines = [t for t in times]
    while len(timelines) > 1:
        t1 = timelines[0]
        pointer = 1
        while pointer < len(timelines):
            t2 = timelines[pointer]
            if better(t2, t1, day):
                timelines = timelines[pointer:]
                break
            pointer += 1
        if pointer == len(timelines):
            return t1
    return timelines[0]
