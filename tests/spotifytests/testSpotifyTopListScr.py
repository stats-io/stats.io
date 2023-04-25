import unittest
from aplication.app import SpotifyTopListScreen


class TestSpotifyTopListScreen(unittest.TestCase):
    def test_create_top_lists(self):
        spotify_top_list_screen = SpotifyTopListScreen()
        spotify_top_list_screen.createTopLists()
        self.assertIsNotNone(spotify_top_list_screen.topTracks)
        self.assertIsNotNone(spotify_top_list_screen.topArtists)
        self.assertIsNotNone(spotify_top_list_screen.recommendations)
