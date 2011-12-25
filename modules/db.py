from datetime import datetime
import logging

from config import conf
from modules.peewee import MySQLDatabase, Model, CharField,\
    DateTimeField, ForeignKeyField, Q

connection = MySQLDatabase(
    host=conf["host"],
    database=conf["database"],
    user=conf["user"],
    passwd=conf["password"]
)


class BaseModel(Model):
    """Base model. To make connection db"""
    class Meta:
        database = connection


class Profession(BaseModel):
    """
       Profession model. To store profession names

       @param name: name of profession

       tablename: profession
    """
    name = CharField()

    class Meta:
        db_table = "profession"

    def __unicode__(self):
        return self.name


class Clan(BaseModel):
    """
       Clan model. To store clans names

       @param name: name of clan

       tablename: clan
    """
    name = CharField()

    class Meta:
        db_table = "clan"

    def __unicode__(self):
        return self.name


class Online(BaseModel):
    """
       Online model. To store online stamp

       @param date: timeshtamp when make parse

       tablename: online
    """
    date = DateTimeField()

    class Meta:
        db_table = "online"

    def __unicode__(self):
        return self.date


class Player(BaseModel):
    """
       Player model. To store player information's

       @param name: name of player
       @param profession: profession id
       @param clan: clan id

       tablename: player
    """
    name = CharField()
    profession = ForeignKeyField(Profession)
    clan = ForeignKeyField(Clan)

    class Meta:
        db_table = "player"

    def __unicode__(self):
        return self.name


class InOnline(BaseModel):
    """
       InOnline model. To store relations between Player and Online models

       @param player: player id
       @param online: online id

       tablename: online_players
    """
    player = ForeignKeyField(Player)
    online = ForeignKeyField(Online)

    class Meta:
        db_table = "online_players"

    def __unicode__(self):
        return '%s/%s' % (self.player, self.online)


connection.connect()


def create_tables():
    """Create all tables"""
    Player.create_table()
    Clan.create_table()
    Profession.create_table()
    Online.create_table()
    InOnline.create_table()

makedate = lambda date: datetime.strptime(date, "%d.%m.%Y")


def get_by_nick(nick=None, frm=None, to=None):
    """
    To get order by nick

    @param nick: player name
    @param frm: filter date from
    @param to: filter date to
    @return dict: dates and player state
    """
    if nick:
        player = Player.select().where(name=nick).get()
        in_online = InOnline.select().order_by('id')
        q_online = Online.select().order_by('id')

        if (frm and frm is not '') and (to and to is not ''):
            online = q_online.where(
                Q(date__gte=makedate(frm)) & Q(date__lte=makedate(to))
            )
            player_online = in_online.where(player=player, online__in=online)
            total = [x.id for x in online]
            dates = [x.date.strftime("%d.%m") for x in online]

        elif frm and frm is not '':
            online = q_online.where(date__gte=makedate(frm))
            player_online = in_online.where(player=player, online__in=online)
            total = [x.id for x in online]
            dates = [x.date.strftime("%d.%m") for x in online]

        elif to and to is not '':
            online = q_online.where(date__lte=makedate(to))
            player_online = in_online.where(player=player, online__in=online)
            total = [x.id for x in online]
            dates = [x.date.strftime("%d.%m") for x in online]

        else:
            player_online = in_online.where(player=player)
            total = [x.id for x in q_online]
            dates = [x.date.strftime("%d.%m") for x in q_online]

        player_all = [p.online_id for p in player_online]
        all = map(lambda x: 1 if x in player_all else 0, total)

        return {'all': dates, 'player': all}
    else:
        return None

def add(name, profa, clan):
    """
    Get or create information in database

    @param name: name user
    @param profa: profession name
    @param clan: clan name
    @return dict:
    """
    clan = Clan.get_or_create(name=clan)
    profa = Profession.get_or_create(name=profa)
    name = Player.get_or_create(name=name, profession=profa, clan=clan)
    logging.warning({"clan": clan, "profa": profa, "name": name})
    return {"clan": clan, "profa": profa, "name": name}

def _online_now(data):
    """
    To append all users who in online now

    @param data: all players in online
    """
    online_now = data['time']
    for player in data["online"]:
        InOnline.create(player=player["name"], online=online_now)
