import unittest
from aplication.app import NetflixUserScreen, setUp


class TestNetflixUserScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_change_screen(self):
        netflix_user_screen = NetflixUserScreen()
        self.app.screen_manager.current = 'Netflix_Main_Screen'
        netflix_user_screen.changeScreen("Netflix_History_Screen")
        self.assertEqual(self.app.screen_manager.current, "Netflix_History_Screen")
        netflix_user_screen.changeScreen("Netflix_Charts_Screen")
        self.assertEqual(self.app.screen_manager.current, "Netflix_Charts_Screen")
        netflix_user_screen.changeScreen("Netflix_Main_Screen")
        self.assertEqual(self.app.screen_manager.current, "Netflix_Main_Screen")

    def test_retrieve_data_from_db(self):
        netflix_user_screen = NetflixUserScreen()
        netflix_user_screen.retrieveDataFromDb()
        self.assertIsNotNone(netflix_user_screen.netflixData)

    def test_back_to_main_screen(self):
        netflix_user_screen = NetflixUserScreen()
        self.app.screen_manager.current = 'Netflix_Main_Screen'
        netflix_user_screen.backToMainScreen()
        self.assertEqual(self.app.screen_manager.current, "Main_Screen")
