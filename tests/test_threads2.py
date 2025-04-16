from multi import Multithreading
from dataclasses import dataclass
import pandas as pd
import random


def multiply(thread_specific_b, a):
    print(f'{a, thread_specific_b = }')
    return thread_specific_b, a, a * thread_specific_b


if __name__ == '__main__':
    amt_threads = 3
    # initialize
    multithreading = Multithreading(multiply, n=amt_threads, update_freq=0.5)

    # define amt_threads and set a unique multiplier for each thread
    multithreading.thread_specific_arguments = list(range(3))

    # add secondary arguments
    multithreading.fill_queue_full(range(9))

    multithreading.start()

