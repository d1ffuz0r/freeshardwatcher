from config import conf
from datetime import datetime
from modules.peewee import MySQLDatabase, Model, CharField,\
    DateTimeField, ForeignKeyField, Q

connection = MySQLDatabase(
    host=conf["host"],
    database=conf["database"],
    user=conf["user"],
    passwd=conf["password"]
)

class BaseModel(Model):
    """
    Base model
    to make connection db
    """
    class Meta:
        database = connection

class Profession(BaseModel):
    """
    Profession model
    to store profession names
    rows:
     - name
    tablename: profession
    """
    name = CharField()

    class Meta:
        db_table = "profession"

    def __unicode__(self):
        return self.name

class Clan(BaseModel):
    """
    Clan model
    to store clans names
    rows:
     - name
    tablename: clan
    """
    name = CharField()

    class Meta:
        db_table = "clan"

    def __unicode__(self):
        return self.name

class Online(BaseModel):
    """
    Online model
    to store online stamp
    rows:
     - date
    tablename: online
    """
    date = DateTimeField()

    class Meta:
        db_table = "online"

    def __unicode__(self):
        return self.date

class Player(BaseModel):
    """
    Player model
    to store player informations
    rows:
    - name
    - profession
    - clan
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
    InOnline model
    to store relations between Player and Online models
    rows:
    - player(id)
    - online(id)
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
    """
    create all tables
    """
    Player.create_table()
    Clan.create_table()
    Profession.create_table()
    Online.create_table()
    InOnline.create_table()

makedate = lambda date: datetime.strptime(date, "%d.%m.%Y")

def get_by_nick(nick=None, frm=None, to=None):
    """
    to get order by nick
    """
    if nick:
        player = Player.select().where(name=nick).get()
        in_online = InOnline.select().order_by('id')
        q_online = Online.select().order_by('id')

        if (frm and frm is not '') and (to and to is not ''):
            online = q_online.where(Q(date__gte=makedate(frm)) & Q(date__lte=makedate(to)))
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

    """
        try:
            if nick:
                #todo need fix!
                player = Player.select().where(name=nick).get()
                online = InOnline.select().where(player=player)
                if dfrom and dto:
                    online = online.join(Online).filter(Q(date__gte=makedate(dfrom)) & Q(date__lte=makedate(dto)))
                elif dfrom:
                    online = online.join(Online).filter(date__gte=makedate(dfrom))
                elif dto:
                    online = online.join(Online).filter(date__lte=makedate(dto))
                else:
                    pass
                return online
            else:
                return None
        except ValueError:
            return None
        """