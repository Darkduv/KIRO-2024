"""Mixing "pocal" and "francois"
Timeline holds the scores of a library for each possible starting time.
initialized as best sum of book scores possibly shipped, considering
library capacity and signup time.
For each book, remember when it would be shipped.

Updated on book shipping by removing this books' score where needed.

runs really slow on instances c and d.
"""
import numpy as np
from collections import defaultdict

from model import Solution
from tools import chrono, Bar

from .full import best

# todo: include previously ignored books

@chrono
class Timeline:
    def __init__(self, library, duration):
        self.library = library
        self.scores = np.zeros((duration))

        # latest time a book will be shipped (-1 is never)
        self.book_times = -np.ones(len(library.books))

        # books[self.index[book.name]] = book
        self.index = defaultdict(lambda: -1)
        self.books = sorted(self.library.books, key=lambda b: b.score, reverse=True)
        for i, book in enumerate(self.books):
            self.index[book.name] = i

        latest = duration - library.signup
        for start in range(latest + 1):
            mi, ma = (library.capacity * (latest - start + i) for i in [0, 1])
            for book in self.books[mi: ma]:
                self.book_times[self.index[book.name]] = start
                self.scores[:start] += book.score

    def ship(self, book):
        for i in range(self.book_times[self.index[book.name]]):
            self.scores[i] -= book.score


@chrono
def ship(instance, order):
    scanned = [False for _ in instance.books]
    shippers = []
    for library, day in order:
        books = sorted(library.books, key=lambda book: book.score)
        load = [book.name for book in books if not scanned[book.name]]
        for name in load:
            scanned[name] = True
        if len(load) > 0:
            shippers.append(Shipper(library.name, load))
    return Solution(shippers)




@chrono
def solve(instance):
    timelines = []
    progress = Bar(len(instance.libraries), "Timelines")
    for lib in instance.libraries:
        timelines.append(Timeline(lib, instance.duration))
        progress.advance(1)

    day = 0
    shipped = []
    progress = Bar(instance.duration, "Ordering")
    while day < instance.duration and len(timelines) > 0:
        lib = best(timelines, day)
        shipped.append((lib.library, day))
        timelines.remove(lib)
        signup = lib.library.signup
        progress.advance(signup)
        day += signup
    return ship(instance, shipped)
