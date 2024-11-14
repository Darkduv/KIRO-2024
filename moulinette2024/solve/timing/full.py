import numpy as np

from tools import chrono


@chrono
def better(t1, t2, day):
    pair = [t1, t2]
    switch = [list(fun(pair)) for fun in [list, reversed]]

    scores = []
    for s, t in switch:
        score = t.scores[day] / (t.library.signup**2)
        if (late := day + t.library.signup) < len(t.scores):
            score += s.scores[late]
        scores.append(score)
    return scores[0] - scores[1]


@chrono
def best(times, day):
    n = len(times)
    scores = np.zeros((n, n))
    for i, s in enumerate(times):
        for j, t in enumerate(times):
            if i == j:
                continue
            scores[i, j] = better(s, t, day)
    return times[np.argmax([sum(r) for r in scores])]
