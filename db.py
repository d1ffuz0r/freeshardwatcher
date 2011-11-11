import sys
sys.path.append("autumn-0.5.1-py2.7.egg")
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:root@localhost:3306/l2planet", echo=False)
session = Session(engine)
Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(ForeignKey('player.id'))
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Player: %s>" % self.name

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

    def __init__(self):
        self.date = datetime.now()

    def __repr__(self):
        return "<Online: %s>" % self.date

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
        session.add(instance)
        session.commit()
        return instance

Base.metadata.create_all(engine)