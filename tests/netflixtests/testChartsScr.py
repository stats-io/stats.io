import unittest
from aplication.app import NetflixChartsScreen, setUp


class TestNetflixChartsScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_create_charts(self):
        netflix_charts_screen = NetflixChartsScreen()
        netflix_charts_screen.createCharts()
        self.assertIsNotNone(netflix_charts_screen.charts)
