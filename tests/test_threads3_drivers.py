from Webdriver import open_drivers, By, WebElement, Driver
from time import sleep
from multi import Multithreading


urls = [
    'https://www.python.org/about/,',
    'https://www.python.org/downloads/',
    'https://www.python.org/doc/',
    'https://www.python.org/community/',
    'https://www.python.org/success-stories/',
    'https://www.python.org/blogs/',
    'https://www.python.org/events/',
    'https://www.python.org/psf-landing/',
    'https://www.python.org/psf/sponsorship/',
    'https://www.python.org/jobs/',
    'https://www.python.org/jobs/types/',
    'https://www.python.org/jobs/categories/',
    'https://www.python.org/jobs/locations/',
    'https://www.python.org/jobs/type/big-data/',
    'https://www.python.org/jobs/type/database/',
    'https://www.python.org/jobs/category/other/',
]


def scrape(driver: Driver, url):
    try:
        driver.visit(url)
        driver.wait_for((By.CLASS_NAME, 'call-to-action'), wait_seconds=10)
        txt = driver.find_element(By.CLASS_NAME, 'call-to-action').text.split('\n')
        sleep(0.3)
        return txt
    except:
        return url


if __name__ == '__main__':
    threads = 3
    m = Multithreading(scrape, update_freq=0.23, n=threads)
    drivers = open_drivers(threads, uc=True, headless=False, use_proxy=False)
    m.fill_queue_full(urls)
    m.thread_specific_arguments = drivers
    m.start()
    for txt in m.results:
        print(txt)

    for d in drivers:
        d.quit()



