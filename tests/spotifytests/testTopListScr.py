import unittest
from aplication.app import SpotifyTopListScreen, setUp
import pandas as pd


class TestSpotifyTopListScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_create_top_lists_top_tracks(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()
        self.assertIsNotNone(spotify_top_list_screen.topTracks)

    def test_create_top_lists_top_artists(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()
        self.assertIsNotNone(spotify_top_list_screen.topArtists)

    def test_create_top_lists_recommendations(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()
        self.assertIsNotNone(spotify_top_list_screen.recommendations)

    def test_top_tracks_sample_data(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()

        with open("./sampledata/spotify_top_tracks.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        fav_songs = spotify_top_list_screen.topTracks
        iter_data = iter(data)
        for i, j in zip(iter_data, fav_songs):
            self.assertEqual(i, j)

    def test_top_artists_sample_data(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()

        with open("./sampledata/spotify_top_artists.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        fav_songs = spotify_top_list_screen.topTracks
        iter_data = iter(data)
        for i, j in zip(iter_data, fav_songs):
            self.assertEqual(i, j)

    def test_recommendations_sample_data(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()

        with open("./sampledata/spotify_recommendations.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        fav_songs = spotify_top_list_screen.topTracks
        iter_data = iter(data)
        for i, j in zip(iter_data, fav_songs):
            self.assertEqual(i, j)
