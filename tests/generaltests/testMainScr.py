import unittest
import sys

sys.path.insert(0, "..")
from aplication.app import setUp


class TestMainScreenNB(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_NetflixButton_click(self):
        self.app.screen_manager.current = "Main_Screen"
        self.app.screen_manager.get_screen("Main_Screen").NetflixNextScreen(None)
        current_screen = self.app.screen_manager.current
        self.assertEqual(current_screen, "Netflix_New_Data_Screen")


class TestMainScreenSB(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_SpotifyButton_click(self):
        self.app.screen_manager.current = "Main_Screen"
        self.app.screen_manager.get_screen("Main_Screen").SpotifyChangeScreen(None)
        current_screen = self.app.screen_manager.current
        self.assertEqual(current_screen, "Spotify_New_Data_Screen")
