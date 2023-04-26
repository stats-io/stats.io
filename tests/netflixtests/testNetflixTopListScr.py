import unittest
from aplication.app import NetflixTopListScreen, setUp


class TestNetflixTopListScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_find_top(self):
        netflix_top_lists_screen = NetflixTopListScreen()
        netflix_top_lists_screen.findTop()
        self.assertIsNotNone(netflix_top_lists_screen.topActors)
        self.assertIsNotNone(netflix_top_lists_screen.topGenres)
        self.assertIsNotNone(netflix_top_lists_screen.topSeries)
        self.assertIsNotNone(netflix_top_lists_screen.mostPopularWatched)
        self.assertIsNotNone(netflix_top_lists_screen.leastPopularWatched)
