# multi package for multithreading and multiprocessing

This package provides convenient reusable code for `threading` and `Multiprocessing` libraries. It creates a wrapper for the standard skeleton of a multi-x module.

## Features
- **Custom Threading Module**: 
  - Initialize `multi.Multithreading`. Here you can set the target function `func` and the number of threads `n` (default 4). Additionally, you can set `update_freq` (default 0.1). This provides functionality for print statements updating the user on the progress that has been made. 
  - After initialization the user needs to fill the queue with tasks using `fill_queue_single` or `fill_queue_full`. The arguments to these methods should be iterable.
  - When the queue is filled the user can use `start` to initialize the threading.
  - Function return values are stored in the `results` attribute.
  - Additionally, the module adds the option of thread-specific arguments to functions.
    - Consider a scraping function `def scrape(driver, url)`. We will initialize the module `m = Multithreading(func=scrape, n=4)`
    - We have 100 urls to scrape, these will be added to the queue. `m.fill_queue_full(urls)`
    - We want to use 4 drivers to scrape these websites. Assert `n=4` in the initialization. Then, start 4 drivers. `drivers = [webdriver.Chrome() for _ in range(4)]`
    - Set drivers to thread-specific arguments. `m.thread_specific_arguments = drivers`
    - Now we can use `m.start()` to scrape the urls using 4 different drivers.
    - If the scraping function has a return value, the values will be stored in `m.results`.

## Installation

To install the package directly from GitHub, run:

```bash
pip install git+https://github.com/HansBerkvens/multi.git@main
```