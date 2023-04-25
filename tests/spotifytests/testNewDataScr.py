import unittest
import os
import sys

sys.path.insert(0, "..")
from aplication.app import setUp, SpotifyNewDataScreen


class TestProcessFile(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def setUp(self):
        self.valid_json_file_path = "./sampledata/small_spotify_history.json"
        self.invalid_file_path = "invalid_file.csv"
        self.invalid_extension_file_path = "invalid_extension_file.txt"

        with open(self.invalid_extension_file_path, "w") as f:
            f.write("This is not a json file.")

    def tearDown(self):
        os.remove(self.invalid_extension_file_path)

    def test_valid_csv_file(self):
        link = SpotifyNewDataScreen.addFile(self.valid_json_file_path)

        with open(link, "r") as file:
            data = file.readlines()

        self.assertEqual(len(data), 2)
        self.assertEqual(data.loc[0, "artistName"], "nome")
        self.assertEqual(data.loc[0, "trackName"], "Tęsknię")
        self.assertEqual(data.loc[1, "artistName"], "Tabb")
        self.assertEqual(data.loc[1, "trackName"], "Ważne")

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            SpotifyNewDataScreen.addFile(self.invalid_file_path)

    def test_invalid_extension_file(self):
        with self.assertRaises(ValueError):
            SpotifyNewDataScreen.addFile(self.invalid_extension_file_path)


class TestMainButtonPressWhenFileExsists(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Button(self):
        self.app.screen_manager.current = "Spotify_New_Data_Screen"
        self.spotify_new_data_screen = self.app.screen_manager.get_screen(
            "Spotify_New_Data_Screen"
        )
        self.spotify_new_data_screen.getFile(None)
        self.app.screen_manager.get_screen("Spotify_New_Data_Screen").SpotifyMainScreen(
            None
        )
        current_screen = self.app.screen_manager.current
        self.assertEqual(
            current_screen == "Spotify_Main_Screen",
            self.spotify_new_data_screen.file_manager != None,
        )


class TestLoadingButtonPressWhenFileExsists(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Button(self):
        self.app.screen_manager.current = "Spotify_New_Data_Screen"
        self.spotify_new_data_screen = self.app.screen_manager.get_screen(
            "Spotify_New_Data_Screen"
        )
        self.spotify_new_data_screen.addFile(None)
        self.app.screen_manager.get_screen(
            "Spotify_New_Data_Screen"
        ).SpotifyLoadingScreen(None)
        current_screen = self.app.screen_manager.current
        self.assertEqual(
            current_screen == "Spotify_Loading_Screen",
            self.spotify_new_data_screen.file_manager != None,
        )
