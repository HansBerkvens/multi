from queue import Queue
import threading
from datetime import datetime
from collections.abc import Iterable


def now():
    return f'{datetime.now().strftime("%H:%M:%S")}\t\t'


class Multithreading:
    def __init__(
            self,
            func: callable,
            n: int = 4,
            update_freq: float = 0.1,
    ):
        self.func: callable = func  # function that needs to be called
        self.n: int = n  # number of threads to use
        self.update_freq: float = update_freq  # frequency of printing an update statement (as percentage)

        self.queue: Queue = Queue()  # initialize queue with arguments
        self.threads: list[threading.Thread] = []  # list of threads
        self.progress: list = [0]  # initialize progress of tasks completed
        self.lock = threading.Lock()  # threading.Lock to thread-safe update self.progress
        self.queue_length = -1
        self.results = []  # list of function outcomes
        self._thread_specific_arguments = self.n * [[]]

    @property
    def thread_specific_arguments(self):
        return self._thread_specific_arguments

    @thread_specific_arguments.setter
    def thread_specific_arguments(self, new_value):
        if not isinstance(new_value, Iterable):
            raise ValueError(f'Multithreading thread_specific_argument was set to {new_value}; which is not Iterable')

        result = []
        for value in new_value:
            if not isinstance(value, Iterable):
                result.append([value])
            else:
                result.append(value)

        self._thread_specific_arguments = result

    def start(self):
        if self.queue.empty():
            raise ValueError('multi.threads.start was called before filling the queue')
        self.queue_length: int = self.queue.qsize()
        self.open_threads()
        self.queue.join()
        self.close_threads()

    def fill_queue_single(self, *args):
        if not isinstance(args, Iterable):
            args = [args]
        self.queue.put(args)

    def fill_queue_full(self, _iterable: Iterable):
        for x in _iterable:
            if not isinstance(x, Iterable) or isinstance(x, str):
                x = [x]
            self.queue.put(x)

    def open_threads(self):
        for i in range(self.n):
            t = threading.Thread(target=self.wrapper, args=self._thread_specific_arguments[i])
            self.threads.append(t)
            t.start()

    def close_threads(self):
        for i in range(self.n):
            self.threads[i].join()

    def wrapper(self, *thread_specific_args):
        while not self.queue.empty():
            args = self.queue.get()
            func_result = None
            try:
                func_result = self.func(*thread_specific_args, *args)
            finally:
                self.queue.task_done()
                with self.lock:
                    if func_result is not None:
                        self.results.append(func_result)
                    self.progress[0] += 1
                    if self.progress[0] % (self.update_freq * self.queue_length) < 1.0 or self.progress[0] == self.queue_length:
                        print(f'{now()}Progress: {self.progress[0]:,}/{self.queue_length:,} tasks completed')



