import unittest
from datetime import datetime
from modules import db
from modules.peewee import SelectQuery


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
        playersonline = db.InOnline(player=db.Player(name="tet2"),
                                    online=online)
        self.assertEqual(playersonline.Meta.db_table, "online_players")
        self.assertEqual(playersonline.__repr__(),
            '<InOnline: <Player: tet2>/%s>' % online.__repr__())

    @unittest.skip("any datatime")
    def test_online(self):
        online = db.Online()
        self.assertEqual(online.Meta.db_table, "online")
        self.assertEqual(online.date, datetime.now())
        self.assertEqual(online.__repr__(), "<Online: %s>" % datetime.now())

    def test_get_by_nick_returns(self):
        request = db.get_by_nick(nick="Lacio")
        self.assertEqual(request["player"], [1, 1, 1, 1, 1, 1, 1, 0, 0])
        self.assertTrue(isinstance(request["all"], SelectQuery))

    def test_get_by_nick_none(self):
        request = db.get_by_nick()
        self.assertIsNone(request)

    def test_get_by_nick_total(self):
        request = db.get_by_nick(nick="Lacio")
        self.assertEqual(request["player"], [1, 1, 1, 1, 1, 1, 1, 0, 0])
        self.assertTrue(isinstance(request["all"], SelectQuery))

    def test_get_by_nick_from(self):
        request = db.get_by_nick(nick="Lacio", frm="15.11.2011")
        self.assertEqual(request["player"], [0, 0])
        self.assertTrue(isinstance(request["all"], SelectQuery))

    def test_get_by_nick_to(self):
        request = db.get_by_nick(nick="Lacio", to="14.11.2011")
        self.assertEqual(request["player"], [1, 1, 1, 1, 1, 1, 1])
        self.assertTrue(isinstance(request["all"], SelectQuery))

    def test_get_by_nick_from_to(self):
        request = db.get_by_nick(nick="Lacio",
                                 frm="12.11.2011",
                                 to="22.11.2011")
        self.assertEqual(request["player"], [1, 1, 1, 1, 1, 1, 1])
        self.assertTrue(isinstance(request["all"], SelectQuery))

        request1 = db.get_by_nick(nick="Lacio",
                                  frm="12.11.2011",
                                  to="27.11.2011")
        self.assertEqual(request1["player"], [1, 1, 1, 1, 1, 1, 1, 0, 0])
        self.assertTrue(isinstance(request1["all"], SelectQuery))

if __name__ == "__main__":
    unittest.main()
