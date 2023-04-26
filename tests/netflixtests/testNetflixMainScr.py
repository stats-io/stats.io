import unittest
from aplication.app import NetflixMainScreen, setUp
import pandas as pd


class TestNetflixMainScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_count_movies(self):
        netflix_main_screen = NetflixMainScreen()
        movies_amount = netflix_main_screen.countMovies()
        self.assertNotEqual(movies_amount, -1)

    def test_count_series(self):
        netflix_main_screen = NetflixMainScreen()
        series_amount = netflix_main_screen.countMovies()
        self.assertNotEqual(series_amount, -1)

    def test_count_movies_sample_data(self):
        netflix_main_screen = NetflixMainScreen()

        with open("./sampledata/local_database.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        movie_count_in_file = 0
        for i in data:
            if i[1] == "film":
                movie_count_in_file = movie_count_in_file + 1

        movie_count = netflix_main_screen.countMovies()
        self.assertEqual(movie_count_in_file, movie_count)

    def test_count_series_sample_data(self):
        netflix_main_screen = NetflixMainScreen()

        with open("./sampledata/local_database.csv") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        series_count_in_file = 0
        for i in data:
            if i[1] == "serial":
                series_count_in_file = series_count_in_file + 1

        series_count = netflix_main_screen.countSeries()
        self.assertEqual(series_count_in_file, series_count)
