#!/usr/bin/env python
import logging
import datetime
from time import sleep

from urllib2 import urlopen, Request, build_opener,\
    install_opener, HTTPCookieProcessor
from re import compile, search, DOTALL, findall
from cookielib import CookieJar

from modules.db import Online, _online_now, add


class Parser(object):
    """Parser class.
    To parse and save in storage information from html pages
    """

    def __init__(self, server='x5', pause=5):
        """
        Initialization class

        @param pause: pause between getting pages, in minutes (default 5)
        """
        #todo to realize work with many servers (asterios, l2, theonline)
        self.url = "http://www.l2planet.ws/?go=online&server=%s" % server
        self.regexp = compile(r'<table\sclass="sort"><thead>.*</thead><tbody>(.*?)</tbody></table>', DOTALL)
        self.regexp2 = compile(r'<tr><td>.*?</td><td>(?P<name>.*?)</td><td>.*?</td><td>.*?</td><td>(?P<prof>.*?)</td><td>(?P<clan>.*?)</td><td>.*?</td></tr>')
        self.pause = pause
        cookie = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie))
        install_opener(opener)
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7; WindowsNT)"}

    def get_content(self):
        """Get content from page"""
        page = urlopen(Request(self.url, headers=self.headers))
        return page.read()

    def parse(self):
        """Parse page"""
        time = Online().create(date=datetime.datetime.now())
        res = {"time": time, "online": []}
        html = search(self.regexp, self.get_content()).group(1).replace('\r\n', '')
        for line in findall(self.regexp2, html):
            res["online"].append(add(line[0], line[1], line[2]))
        _online_now(res)

    def start(self):
        """Start engine"""
        __all__ = 0
        while True:
            __all__ += 1
            self.parse()
            print __all__
            sleep(60 * self.pause)

    def get(self):
        """Stub for testing"""
        self.parse()

if __name__ == '__main__':
    parser = Parser(pause=30)
    parser.start()
