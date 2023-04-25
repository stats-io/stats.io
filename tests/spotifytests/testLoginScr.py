import unittest
from unittest.mock import MagicMock
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys

sys.path.insert(0, "..")
from aplication.app import setUp, SpotifyLoginScreen


os.environ["SPOTIPY_CLIENT_ID"] = "#key"
os.environ["SPOTIPY_CLIENT_SECRET"] = "#key"
os.environ["SPOTIPY_REDIRECT_URI"] = "localhost"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))


class TestButtons(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testSkipButton(self):
        self.app.screen_manager.current = "Spotify_Login_Screen"
        self.spotify_login_screen = self.app.screen_manager.get_screen(
            "Spotify_Login_Screen"
        )
        self.spotify_login_screen.spotifyMainScreenChange(None)
        current_screen = self.app.screen_manager.current
        self.assertEqual(current_screen == "Spotify_Main_Screen", True)

    def test_successful_login(self):
        sp.auth_manager.get_access_token = MagicMock(return_value="test_token")
        self.app.screen_manager.current = "Spotify_Login_Screen"
        self.spotify_login_screen = self.app.screen_manager.get_screen(
            "Spotify_Login_Screen"
        )
        self.spotify_login_screen.handleLogin("test_code")
        self.assertEqual(
            sp.auth_manager.get_cached_token()["access_token"], "test_token"
        )

    def test_failed_login(self):
        sp.auth_manager.get_access_token = MagicMock(return_value=None)
        self.app.screen_manager.current = "Spotify_Login_Screen"
        self.spotify_login_screen = self.app.screen_manager.get_screen(
            "Spotify_Login_Screen"
        )
        self.spotify_login_screen.handleLogin("invalid_code")
        self.assertIsNone(sp.auth_manager.get_cached_token())
