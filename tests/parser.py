import unittest
from src.engine import Parser
from src import db

class TestsParser(unittest.TestCase):

    def setUp(self):
        self.parser1 = Parser(server="x5")
        self.parser2 = Parser(server="x1")
        self.parser = Parser(server="x5")
        self.parser.url = "file:///F:/x5.htm"

    def test_create(self):
        self.assertIsNotNone(self.parser)

    def test_params(self):
        self.assertEqual(self.parser1.url, "http://www.l2planet.ws/?go=online&server=x5")
        self.assertEqual(self.parser2.url, "http://www.l2planet.ws/?go=online&server=x1")
        self.assertEqual(self.parser.pause, 0)
        self.assertEqual(self.parser.headers, {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7; WindowsNT)"})

    def test_get_content(self):
        self.assertIn("<body>", self.parser.get_content())

    def test_parse(self):
        result = self.parser.parse()
        profile = str({'clan': db.Clan(name="DwarfsInc"),
                   'profa': db.Profa(name="Doombringer"),
                   'name': db.Player(name="NOD")})
  