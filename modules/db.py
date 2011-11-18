from datetime import datetime
from modules.peewee import MySQLDatabase, Model, CharField,\
    DateTimeField, ForeignKeyField, Q

connection = MySQLDatabase(
    host="mysql.alwaysdata.com",
    database='freeshardwatcher_db',
    user="freeshardwatcher",
    passwd="p300aj2"
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
    date = DateTimeField(default=datetime.now())

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

def all_online():
    """
    to get list all stamps a Online
    """
    return Online.select().order_by('id')

def get_by_nick(nick, dfrom=False, dto=False):
    """
    to get order by nick
    """
    #todo ned refactoring
    try:
        player = Player.select().where(name=nick).get()
        q = InOnline.select().where(player=player)
        if dfrom and dto:
            q = q.join(Online).where(Q(date__gte=makedate(dfrom)) & Q(date__lte=makedate(dto)))
        return q
    except ValueError:
        return None