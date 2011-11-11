#!/usr/bin/env python
from time import sleep
from urllib2 import urlopen, Request, build_opener,\
    install_opener, HTTPCookieProcessor
from re import compile, search, DOTALL, findall
from cookielib import CookieJar
from db import get_or_create, session, Clan, Player,\
    Profa, Profile, PlayersOnline, Online

class Parser(object):
    def __init__(self, server, pause=0):
        self.url = "http://www.l2planet.ws/?go=online&server={server}".format(server=server)
        self.regexp = compile(r'<table\sclass="sort"><thead>.*</thead><tbody>(.*?)</tbody></table>', DOTALL)
        self.regexp2 = compile(r'<tr><td>.*?</td><td>(?P<name>.*?)</td><td>.*?</td><td>.*?</td><td>(?P<prof>.*?)</td><td>(?P<clan>.*?)</td><td>.*?</td></tr>')
        self.pause = pause
        cookie = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie))
        install_opener(opener)
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7; WindowsNT)"}

    def get_content(self):
         page = urlopen(Request(self.url, headers=self.headers))
         return page.read()

    def add(self, name, profa, clan):
        clan = get_or_create(session, Clan, name=clan)
        name = get_or_create(session, Player, name=name)
        profa = get_or_create(session, Profa, name=profa)
        profile = get_or_create(session, Profile, **{"clan": clan.id,
                                                     "name": name.id,
                                                     "profa": profa.id})
        return {"clan": clan, "profa": profa, "name": name}

    def _online_now(self, data):
        online_now_id = data['time'].id
        for player in data["online"]:
            get_or_create(session, PlayersOnline, **{"player_id": player["name"].id,
                                                     "online_id": online_now_id})

    def parse(self):
        time = Online()
        session.add(time)
        res = {"time": time, "online": []}
        html = search(self.regexp, self.get_content()).group(1).replace('\r\n','')
        for line in findall(self.regexp2, html):
            res["online"].append(self.add(line[0], line[1], line[2]))
        self._online_now(res)

    def start(self):
        __all__ = 0
        while True:
            __all__ += 1
            self.parse()
            print __all__
            sleep(60*self.pause)

    def get(self):
        self.parse()

if __name__ == '__main__':
    parser = Parser(pause=5, server="x5")#profa="Doomcryer", clan="DwarfsInc"
    parser.start()
    #parser.get()
