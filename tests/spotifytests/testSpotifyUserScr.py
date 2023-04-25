import unittest
from aplication.app import SpotifyUserScreen, setUp


class TestSpotifyUserScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_change_screen(self):
        spotify_user_screen = SpotifyUserScreen()
        self.app.screen_manager.current = "Spotify_Main_Screen"
        spotify_user_screen.changeScreen("Spotify_Top_List_Screen")
        self.assertEqual(self.app.screen_manager.current, "Spotify_Top_List_Screen")
        spotify_user_screen.changeScreen("Spotify_History_Screen")
        self.assertEqual(self.app.screen_manager.current, "Spotify_History_Screen")
        spotify_user_screen.changeScreen("Spotify_Main_Screen")
        self.assertEqual(self.app.screen_manager.current, "Spotify_Main_Screen")

    def test_back_to_main_screen(self):
        spotify_user_screen = SpotifyUserScreen()
        self.app.screen_manager.current = "Spotify_Main_Screen"
        spotify_user_screen.backToMainScreen()
        self.assertEqual(self.app.screen_manager.current, "Main_Screen")

    def test_data(self):
        spotify_user_screen = SpotifyUserScreen()

        self.assertIsNotNone(spotify_user_screen.spotifyData)
        self.assertIsNotNone(spotify_user_screen.historyData)
