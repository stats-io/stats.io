import unittest
import json
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

sys.path.insert(0, "..")
from aplication.app import SpotifyProcessData


os.environ["SPOTIPY_CLIENT_ID"] = "#key"
os.environ["SPOTIPY_CLIENT_SECRET"] = "#key"
os.environ["SPOTIPY_REDIRECT_URI"] = "localhost"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))


class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.app = SpotifyProcessData(sp)

    def test_load_json_file(self):
        test_file = "test_file.json"
        with open(test_file, "w") as f:
            json.dump({"test": "data"}, f)

        result = self.app.load_json_file(test_file)
        self.assertIsInstance(result, dict)
        self.assertIn("test", result)

        os.remove(test_file)

    def test_last_fifty_data_csv(self):
        self.app.load_last_fifty_tracks_data()
        self.assertTrue(os.path.isfile("lastfiftydata.csv"))

        with open("lastfiftydata.csv", "r") as csvfile:
            reader = pd.read_csv(csvfile)
            header = next(reader)
            first_row = next(reader)
            self.assertIsNotNone(first_row)

    def test_history_csv(self):
        self.app.load_history_data()
        self.assertTrue(os.path.isfile("history.csv"))

        with open("history.csv", "r") as csvfile:
            reader = pd.read_csv(csvfile)
            header = next(reader)
            first_row = next(reader)
            self.assertIsNotNone(first_row)
