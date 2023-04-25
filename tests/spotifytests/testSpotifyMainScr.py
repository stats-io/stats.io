import unittest
from aplication.app import SpotifyMainScreen


class TestSpotifyMainScreen(unittest.TestCase):
    def test_count_minutes(self):
        spotify_main_screen = SpotifyMainScreen()
        self.assertNotEqual(spotify_main_screen.countMinutes(), 0)

    def test_choose_day_of_week(self):
        spotify_main_screen = SpotifyMainScreen()
        self.assertIsNotNone(spotify_main_screen.chooseDayOdWeek())
