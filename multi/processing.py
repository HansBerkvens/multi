from multiprocessing import Pool
from collections.abc import Iterable


class Multiprocessing:
    def __init__(
            self,
            func: callable,
            n: int,
            update_freq: float = 0.1,
            iterable: Iterable | None = None
    ):
        self.func: callable = func  # function that needs to be called
        self.n: int = n  # number of processes to use
        self.update_freq: float = update_freq  # frequency of printing an update statement (as percentage)
        self.iterable: Iterable | None = iterable
        self.results = None

    def start(self):
        with Pool(self.n) as pool:
            results = pool.map(self.func, self.iterable)

        self.results = results




