#!/usr/bin/env python
import logging
import datetime
from time import sleep
from urllib2 import urlopen, Request, build_opener,\
    install_opener, HTTPCookieProcessor
from re import compile, search, DOTALL, findall
from cookielib import CookieJar
from modules.db import Player, Clan, Online,\
    InOnline, Profession

class Parser(object):
    """
    Parser class
    to parse and save in storage information from html pages
    """
    def __init__(self, pause=0):
        """
        Initialization class
        params:
        - server(so far to work be with server(l2planer.ws))
        - pause(pause between getting pages, in minutes)
        """
        #todo to realize work with many servers (asterios, l2, theonline)
        self.url = "http://www.l2planet.ws/?go=online&server=x5"
        self.regexp = compile(r'<table\sclass="sort"><thead>.*</thead><tbody>(.*?)</tbody></table>', DOTALL)
        self.regexp2 = compile(r'<tr><td>.*?</td><td>(?P<name>.*?)</td><td>.*?</td><td>.*?</td><td>(?P<prof>.*?)</td><td>(?P<clan>.*?)</td><td>.*?</td></tr>')
        self.pause = pause
        cookie = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie))
        install_opener(opener)
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7; WindowsNT)"}

    def get_content(self):
        """
        get content from page
        """
        page = urlopen(Request(self.url, headers=self.headers))
        return page.read()

    def add(self, name, profa, clan):
        """
        get or create information in database
        """
        clan = Clan.get_or_create(name=clan)
        profa = Profession.get_or_create(name=profa)
        name = Player.get_or_create(name=name, profession=profa, clan=clan)
        logging.warning({"clan": clan, "profa": profa, "name": name})
        return {"clan": clan, "profa": profa, "name": name}

    def _online_now(self, data):
        """
        to append all users who in online now
        """
        online_now = data['time']
        for player in data["online"]:
            InOnline.create(player=player["name"], online=online_now)

    def parse(self):
        """
        parse page
        """
        time = Online(date=datetime.datetime.now()).create()
        res = {"time": time, "online": []}
        html = search(self.regexp, self.get_content()).group(1).replace('\r\n','')
        for line in findall(self.regexp2, html):
            res["online"].append(self.add(line[0], line[1], line[2]))
        self._online_now(res)

    def start(self):
        """
        start engine
        """
        __all__ = 0
        while True:
            __all__ += 1
            self.parse()
            print __all__
            sleep(60*self.pause)

    def get(self):
        """
        stub for testings
        """
        self.parse()

if __name__ == '__main__':
    parser = Parser(pause=5)
    parser.start()
