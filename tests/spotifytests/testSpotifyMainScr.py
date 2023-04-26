import unittest
import pandas as pd
from aplication.app import SpotifyMainScreen, setUp


class TestSpotifyMainScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_count_minutes_error(self):
        spotify_main_screen = SpotifyMainScreen()
        self.assertNotEqual(spotify_main_screen.countMinutes(), -1)

    def test_count_minutes_sample_data(self):
        spotify_main_screen = SpotifyMainScreen()
        with open("./sampledata/spotify_history.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        estimated_time = 0
        for i in data:
            estimated_time = estimated_time + i[3]

        time = spotify_main_screen.countMinutes()
        self.assertEqual(time, estimated_time)

    def test_choose_day_of_week(self):
        spotify_main_screen = SpotifyMainScreen()
        self.assertIsNotNone(spotify_main_screen.chooseDayOdWeek())
