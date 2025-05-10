import unittest
import os
from config import load_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        if os.path.isfile("trackerconf.toml"):
            os.rename("trackerconf.toml", "trackerconf.toml.bak")

    def restore(self):
        if os.path.isfile("trackerconf.toml"):
            os.remove("trackerconf.toml")
        if os.path.isfile("trackerconf.toml.bak"):
            os.rename("trackerconf.toml.bak", "trackerconf.toml")

    def test_load_config_file_not_found(self):
        result = load_config()
        self.assertEqual(result["currency"], "€")
        self.restore()

    def test_load_config_valid_file(self):
        with open("trackerconf.toml", "w") as f:
            f.write('dbfile="filu"')
        result = load_config()
        self.assertEqual(result["dbfile"], "filu")
        self.restore()

    def test_load_config_invalid_format(self):
        with open("trackerconf.toml", "w") as f:
            f.write('dbfile="filu')
        result = load_config()
        self.assertEqual(result["dbfile"], "database.db")
        self.restore()

    def test_load_config_wrong_type(self):
        with open("trackerconf.toml", "w") as f:
            f.write("dbfile=2")
        result = load_config()
        self.assertEqual(result["dbfile"], "database.db")
        self.restore()
