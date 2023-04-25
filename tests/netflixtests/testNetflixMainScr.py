import unittest
from aplication.app import NetflixMainScreen


class TestNetflixMainScreen(unittest.TestCase):
    def test_count_movies(self):
        netflix_main_screen = NetflixMainScreen()
        movies_amount = netflix_main_screen.countMovies()
        self.assertNotEqual(movies_amount, -1)

    def test_count_series(self):
        netflix_main_screen = NetflixMainScreen()
        series_amount = netflix_main_screen.countMovies()
        self.assertNotEqual(series_amount, -1)
