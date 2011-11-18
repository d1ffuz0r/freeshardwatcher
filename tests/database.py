import unittest
from datetime import datetime
from modules import db

class TestsDatabase(unittest.TestCase):

    def test_player(self):
        player = db.Player(name="test")

        self.assertEqual(player.Meta.db_table, "player")
        self.assertEqual(player.name, "test")
        self.assertEqual(player.__repr__(), "<Player: test>")

    def test_clan(self):
        clan = db.Clan(name="testclan")

        self.assertEqual(clan.Meta.db_table, "clan")
        self.assertEqual(clan.name, "testclan")
        self.assertEqual(clan.__repr__(), "<Clan: testclan>")

    def test_profa(self):
        profa = db.Profession(name="doomcryer")

        self.assertEqual(profa.Meta.db_table, "profession")
        self.assertEqual(profa.name, "doomcryer")
        self.assertEqual(profa.__repr__(), "<Profession: doomcryer>")

    def test_players_online(self):
        online = db.Online()
        playersonline = db.InOnline(player=db.Player(name="tet2"), online=online)
        self.assertEqual(playersonline.Meta.db_table, "online_players")
        self.assertEqual(playersonline.__repr__(), '<InOnline: <Player: tet2>/%s>' % online.__repr__())

    @unittest.skip("any datatime")
    def test_online(self):
        online = db.Online().create()
        self.assertEqual(online.Meta.db_table, "online")
        self.assertEqual(online.date, datetime.now())
        self.assertEqual(online.__repr__(), "<Online: %s>" % datetime.now())

if __name__ == "__main__":
    unittest.main()