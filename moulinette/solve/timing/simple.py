from tools import chrono


@chrono
def best(timelines, day):
    lib, score = None, -1
    for timeline in timelines:
        if (s := timeline.scores[day]) > score:
            lib, score = timeline, s
    return lib
