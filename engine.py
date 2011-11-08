#!/usr/bin/env python
import logging
from urllib2 import urlopen, Request, build_opener, install_opener, HTTPCookieProcessor
from re import compile, search, DOTALL, findall
from cookielib import CookieJar
from time import sleep, time
from datetime import datetime
from sqlalchemy import *
from sqlalchemy import desc
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine("mysql://root:root@localhost:3306/l2planet", echo=False)
session = Session(engine)
Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(ForeignKey('player.id'), unique=True)
    profa = Column(ForeignKey('profession.id'))
    clan = Column(ForeignKey('clan.id'))

    def __init__(self, name, profa, clan):
        self.name = name
        self.profa = profa
        self.clan = clan
        
    def __repr__(self):
        return "<Profile: %s/%s/%s>" % (self.name, self.profa, self.clan)

class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Player: %s>" % (self.name)

class Profa(Base):
    __tablename__ = "profession"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Profa: %s>" % self.name

class Clan(Base):
    __tablename__ = "clan"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Clan: %s>" % self.name

class Online(Base):
    __tablename__ = "online"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    """    players_online = relationship("PlayersOnline",
                                primaryjoin="and_(Online.id == PlayersOnline.online_id)",
                                cascade="all, delete-orphan",
                                backref='online')
    players = association_proxy("online_players", "online_id")
    """
    def __init__(self):
        self.date = datetime.now()

class PlayersOnline(Base):
    __tablename__ = "online_players"

    player_id = Column(Integer, ForeignKey('player.id'), primary_key=True)
    online_id = Column(Integer, ForeignKey('online.id'), primary_key=True)

    def __init__(self, player_id, online_id):
        self.player_id = player_id
        self.online_id = online_id

    def __repr__(self):
        return "<PlayersInOnline: %s(%s)>" % (self.online_id, self.player_id)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance

def get_or_pass(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    instance = model(**kwargs)
    if instance not in session:
        session.add(instance)

#Base.metadata.create_all(engine)

class Parser(object):
    def __init__(self, server, pause, profa=None, clan=None):
        self.url = "http://www.l2planet.ws/?go=online&server={server}".format(server=server)
        self.regexp = compile(r'<table\sclass="sort"><thead>.*</thead><tbody>(.*?)</tbody></table>', DOTALL)
        self.regexp2 = compile(r'<tr><td>.*?</td><td>(?P<name>.*?)</td><td>.*?</td><td>.*?</td><td>(?P<prof>.*?)</td><td>(?P<clan>.*?)</td><td>.*?</td></tr>')
        self.pause = pause
        self.profa = profa
        self.clan = clan
        cookie = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie))
        install_opener(opener)
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7; WindowsNT)"}

    def _get_content(self):
         page = urlopen(Request(self.url, headers=self.headers))
         return page.read()

    def _add(self, name, profa, clan):
        clan = get_or_create(session, Clan, name=clan)
        name = get_or_create(session, Player, name=name)
        profa = get_or_create(session, Profa, name=profa)

        get_or_pass(session, Profile, **{"clan": clan.id, "name": name.id, "profa": profa.id})
        session.add_all([clan, name, profa])

        return {"clan": clan, "profa": profa, "name": name}

    def _online_now(self, data):
        online_now_id = data['time'].id
        for player in data["online"][:-1]:
            online_user = PlayersOnline(player_id=player["name"].id, online_id=online_now_id)
            session.add(online_user)

    def parse(self):
        online = Online()
        session.add(online)
        res = {"time": online, "online": []}
        html = search(self.regexp, self._get_content()).group(1).replace('\r\n','')

        for line in findall(self.regexp2, html):
            name = line[0]
            profa, clan = line[1], line[2]
            if self.profa and self.clan:
                if profa == self.profa and clan == self.clan:
                    res["online"].append(self._add(name, profa, clan))
            elif self.profa:
                if profa == self.profa:
                    res["online"].append(self._add(name, profa, clan))
            elif self.clan:
                if clan == self.clan:
                    res["online"].append(self._add(name, profa, clan))
            else:
                res["online"].append(self._add(name, profa, clan))
        self._online_now(res)

    def start(self):
        __all__ = 0
        while True:
            __all__ += 1
            self.parse()
            print __all__
            sleep(60*self.pause)

if __name__ == '__main__':
    parser = Parser(pause=5, server="x5")#profa="Doomcryer", clan="DwarfsInc"
    parser.start()
    session.commit()
