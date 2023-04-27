import unittest
from aplication.app import NetflixTopListScreen, setUp
import pandas as pd


class TestNetflixTopListScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_find_top_actors(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.topActors)

    def test_find_top_genres(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.topGenres)

    def test_find_top_series(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.topSeries)

    def test_find_most_popular_watched(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.mostPopularWatched)

    def test_find_least_popular_watched(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.leastPopularWatched)

    def test_find_most_popular_watched_sample_data(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()

        with open("./sampledata/netflix_most_popular_watched") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        most_popular = netflix_top_lists_screen.mostPopularWatched
        iter_data = iter(data)
        for i, j in zip(iter_data, most_popular):
            self.assertEqual(i, j)

    def test_find_least_popular_watched_sample_data(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()

        with open("./sampledata/netflix_least_popular_watched") as file:
            reader = pd.read_csv(file)
            data = reader.values.tolist()

        most_popular = netflix_top_lists_screen.leastPopularWatched
        iter_data = iter(data)
        for i, j in zip(iter_data, most_popular):
            self.assertEqual(i, j)
