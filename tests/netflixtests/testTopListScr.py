import unittest
from aplication.app import NetflixTopListScreen, setUp


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
