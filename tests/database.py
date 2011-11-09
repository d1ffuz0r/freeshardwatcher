import unittest
from datetime import datetime
from src import db

class TestsDatabase(unittest.TestCase):

    def test_player(self):
        player = db.Player(name="test")

        self.assertEqual(player.__tablename__, "player")
        self.assertEqual(player.name, "test")
        self.assertEqual(player.__repr__(), "<Player: test>")

    def test_clan(self):
        clan = db.Clan(name="testclan")

        self.assertEqual(clan.__tablename__, "clan")
        self.assertEqual(clan.name, "testclan")
        self.assertEqual(clan.__repr__(), "<Clan: testclan>")

    def test_profa(self):
        profa = db.Profa(name="doomcryer")

        self.assertEqual(profa.__tablename__, "profession")
        self.assertEqual(profa.name, "doomcryer")
        self.assertEqual(profa.__repr__(), "<Profa: doomcryer>")

    def test_profile(self):
        profile = db.Profile(name=db.Player(name="test1"),
            profa=db.Profa(name="test1"),
            clan=db.Clan(name="test1")
        )
        self.assertEqual(profile.__tablename__, "profiles")
        self.assertEqual(profile.__repr__(), "<Profile: <Player: test1>/<Profa: test1>/<Clan: test1>>")

    def test_players_online(self):
        online = db.Online()
        playersonline = db.PlayersOnline(player_id=db.Player(name="tet2"), online_id=online)
        self.assertEqual(playersonline.__tablename__, "online_players")
        self.assertEqual(playersonline.__repr__(), '<PlayersInOnline: %s(<Player: tet2>)>' % online.__repr__())

    def test_getorcreate(self):
        creater = db.get_or_create(session=db.session, model=db.Player, name="test")
        self.assertEqual(creater.__repr__(), "<Player: test>")

    #@unittest.skip("any datatime")
    def test_online(self):
        online = db.Online()
        self.assertEqual(online.__tablename__, "online")
        self.assertEqual(online.date, datetime.now())
        self.assertEqual(online.__repr__(), "<Online: %s>" % datetime.now())