import unittest
from aplication.app import NetflixChartsScreen


class TestNetflixChartsScreen(unittest.TestCase):
    def test_create_charts(self):
        netflix_charts_screen = NetflixChartsScreen()
        netflix_charts_screen.createCharts()
        self.assertIsNotNone(netflix_charts_screen.charts)
