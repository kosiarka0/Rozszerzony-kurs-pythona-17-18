from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import re
import queue
from tqdm import tqdm
from chardet import detect
from ssl import CertificateError


def is_valid_web_address(address):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return (isinstance(address, str) or isinstance(address, bytes)) and bool(re.match(regex, address))


def get_site_content(site):
    exception_tuple = (
        ConnectionResetError, HTTPError, URLError, CertificateError, ConnectionAbortedError, UnicodeDecodeError)
    try:

        site_request = Request(site, headers={'User-agent': 'Mozilla/5.0'})

        site_response = urlopen(site_request)
        if not site_response.status == 200:
            return ""
        site_content_bites = site_response.read()
        coding = detect(site_content_bites).get("encoding")
        if not coding:
            return ""
        site_content = site_content_bites.decode(coding)
        site_response.close()
        return site_content
    except exception_tuple:
        return ""


def crawler(site, fun, depth=3):
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.things = []

        def error(self, message):
            pass

        def handle_starttag(self, tag, attrs):
            # print("Encountered a start tag:", tag)
            if tag == "a":
                for name, value in attrs:
                    if name == "href" and is_valid_web_address(value):
                        self.things.append(value)
            if tag == "p":
                pass

        def __iter__(self):
            return iter(self.things)

    address_que = queue.Queue()
    address_que.put_nowait((site, 0))
    visited = set()
    my_p = MyHTMLParser()

    while not address_que.empty():
        act_site, act_depth = address_que.get_nowait()

        if act_depth >= depth or act_site in visited:
            address_que.task_done()
            continue

        visited.add(act_site)
        site_content = get_site_content(act_site)

        yield act_site, "Act_depth:{}".format(act_depth), fun(site_content)
        my_p.reset()
        my_p.feed(site_content)
        for sub_site in my_p:
            address_que.put_nowait((sub_site, act_depth + 1))
        address_que.task_done()
    print("Total sites watched : {}.".format(len(visited)))


def my_fnct(site):
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.things = []

        def error(self, message):
            pass

        def handle_starttag(self, tag, attrs):
            if tag == "p":
                for name, val in attrs:
                    if "python" in val.lower():
                        yield val

        def __iter__(self):
            return iter(self.things)

        def handle_data(self, data):
            if "python" in data.lower():
                self.things.append(data)

    my_p = MyHTMLParser()
    my_p.feed(site)
    return list(my_p)


if __name__ == "__main__":
    for s, d, result in tqdm(crawler("http://grining.bblog.pl/", my_fnct, 5)):
        if result:
            print("I found python content on site {0} in depth {1}! Here it is:\n{2}".format(s, d, result))
