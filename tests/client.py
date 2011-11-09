import unittest
from src.cli import Client

class ClientTests(unittest.TestCase):
    def setUp(self):
        self.cli = Client()

    def test_client(self):
        self.assertIsNotNone(self.cli)

    def test_get_all_times(self):
        self.assertIsNotNone(self.cli.all_online())

    def test_get_by_nick_true(self):
        query = self.cli.get_by_nick(nick="Lacio")

        self.assertIsNotNone(query)

        ALL = [int(t.id) for t in self.cli.all_online()]
        PLAYER = [int(t1.online_id) for t1 in query]

        print map(lambda x,y: (x, 1 if y is x else 0), ALL,PLAYER)

    def test_get_by_nick_false(self):
        self.assertIsNone(self.cli.get_by_nick(nick="Preree"))