import re

from tqdm import tqdm
import requests
import bs4
from itertools import chain
from multiprocessing import Process
from contextlib import suppress


def is_valid_web_address(address):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return (isinstance(address, str) or isinstance(address, bytes)) and bool(re.match(regex, address))


def get_site_content(site_url):
    if not is_valid_web_address(site_url):
        return ""
    try:
        req = requests.get(site_url)
    except:
        return ""

    if not req.status_code == 200:
        req.close()
        return ""
    result_content = req.text
    req.close()
    return result_content


def act_starting_on_site(site, fun, *, depth=3, processes_num=6):
    from multiprocessing import JoinableQueue as Queue
    crawler_to_worker_que = Queue()
    worker_to_screamer_que = Queue()

    workers = [Process(target=worker, args=(fun, crawler_to_worker_que, worker_to_screamer_que)) for _ in
               range(processes_num)]
    for worker_process in workers:
        worker_process.daemon = True
        worker_process.start()

    crawler_process = Process(target=crawler, args=(site, crawler_to_worker_que, depth))
    crawler_process.daemon = True
    crawler_process.start()

    queue_closer = Process(target=crawler, args=(site, crawler_to_worker_que, depth))
    queue_closer.daemon = True
    queue_closer.start()

    return screamer(worker_to_screamer_que)


def crawler(site, todo_que, depth=3):
    from queue import Queue
    address_que = Queue()
    address_que.put_nowait((site, 0))
    visited = set()

    while not address_que.empty():
        act_site, act_depth = address_que.get_nowait()

        if act_depth >= depth or act_site in visited:
            address_que.task_done()
            continue

        visited.add(act_site)
        site_content = get_site_content(act_site)

        todo_que.put((site_content, act_depth, act_site))
        soup = bs4.BeautifulSoup(site_content, "html.parser")
        for tag in soup.find_all("a", attrs={"href": True}):
            address_que.put_nowait((tag.get("href"), act_depth + 1))
        address_que.task_done()


def screamer(result_que):
    while True:
        yield result_que.get()
        result_que.task_done()


def worker(todo_function, in_que, out_que):
    while True:
        content, depth, site = in_que.get()
        out_que.put((site, depth, list(todo_function(content))))
        in_que.task_done()


def que_closer(queues_to_wait_for):
    for que in queues_to_wait_for:
        que.join()


def python_finder(html_content):
    try:
        soup = bs4.BeautifulSoup(html_content, "html.parser")
    except NotImplementedError:
        return []

    for script in soup(["script", "style"]):
        script.extract()

    texts = soup.find_all(text=True)

    return ("...{}...".format(text_part) for text_part in
            chain.from_iterable(re.findall(".{1,40}python.{1,40}", text, flags=re.IGNORECASE) for text in texts))


if __name__ == "__main__":
    for s, d, result in tqdm(act_starting_on_site("https://www.photoblog.com/", python_finder, depth=5)):
        res_list = list(result)
        if res_list:
            print("I found python content on site {0} in depth {1}!".format(s, d))
            for res in res_list:
                print(res)
