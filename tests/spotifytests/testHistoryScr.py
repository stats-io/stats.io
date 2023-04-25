import unittest
import pandas as pd
import sys

sys.path.insert(0, "..")
from aplication.app import SpotifyHistoryScreen, setUp


class SpotifyList(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testSpotifyList(self):
        SHS = SpotifyHistoryScreen()
        SHS.loadHistory("./sampledata/spotify_history.json")

        with open("./sampledata/spotify_history.csv") as file:
            reader = pd.read_csv(file)
            data = list(reader)

        all_songs = []
        for i in SHS.list_of_songs.children:
            all_songs.append(i.text)

        for l1, l2 in zip(data, all_songs):
            self.assertEqual(l1, l2)


class SpotifySearch(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testSpotifyListSearch(self):
        SHS = SpotifyHistoryScreen()
        SHS.loadHistory("./sampledata/spotify_history.json")
        SHS.searchTitle("Still D.R.E.")

        with open("./sampledata/spotify_search_expected.csv") as file:
            reader = pd.read_csv(file)
            data = list(reader)

        searched = []
        for i in SHS.list_of_songs.children:
            searched.append(i.text)

        for l1, l2 in zip(data, searched):
            self.assertEqual(l1, l2)
