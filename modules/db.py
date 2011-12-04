from datetime import datetime

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
    """Profession model. To store profession names

       Keyword arguments:
       name -- profession name

       tablename: profession
    """
    name = CharField()

    class Meta:
        db_table = "profession"

    def __unicode__(self):
        return self.name


class Clan(BaseModel):
    """Clan model. To store clans names

       Keyword arguments:
       name -- clan name

       tablename: clan
    """
    name = CharField()

    class Meta:
        db_table = "clan"

    def __unicode__(self):
        return self.name


class Online(BaseModel):
    """Online model. To store online stamp

       Keyword arguments:
       date -- datetime stamp

       tablename: online
    """
    date = DateTimeField()

    class Meta:
        db_table = "online"

    def __unicode__(self):
        return self.date


class Player(BaseModel):
    """Player model. To store player information's

       Keyword arguments:
       name -- player nmame
       profession -- profession id
       clan -- clan id

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
    """InOnline model. To store relations between Player and Online models

       Keyword arguments:
       player -- player id
       online -- inline id

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
    """To get order by nick

       Keyword arguments:
       nick -- player name
       frm -- filter date from
       to -- filter date to

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
