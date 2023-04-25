import unittest
import sys

sys.path.insert(0, "..")
from aplication.app import setUp


class testNetflixNewDataScreenCSV(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_CSV(self):
        self.netflix_new_data_screen = self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        )
        self.netflix_new_data_screen.addFile(None)
        self.file = self.netflix_new_data_screen.file_manager
        self.assertEqual(self.file.ext, [".csv"])


class TestLoadingButtonPressWhenFileExsists(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Button(self):
        self.app.screen_manager.current = "Netflix_New_Data_Screen"
        self.netflix_new_data_screen = self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        )
        self.netflix_new_data_screen.addFile(None)
        self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        ).NetflixloadingScreen(None)
        current_screen = self.app.screen_manager.current
        self.assertEqual(
            current_screen == "Netflix_Loading_Screen",
            self.netflix_new_data_screen.file_manager != None,
        )


class TestMainButtonPressWhenFileExsists(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Button(self):
        self.app.screen_manager.current = "Netflix_New_Data_Screen"
        self.netflix_new_data_screen = self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        )
        self.netflix_new_data_screen.getFile(None)
        self.app.screen_manager.get_screen("Netflix_New_Data_Screen").NetflixMainScreen(
            None
        )
        current_screen = self.app.screen_manager.current
        self.assertEqual(
            current_screen == "Netflix_Main_Screen",
            self.netflix_new_data_screen.file_manager != None,
        )


class FormatofUserFileIsGood(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Format(self):
        self.netflix_new_data_screen = self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        )
        self.netflix_new_data_screen.addFile(None)
        self.filepath = self.netflix_new_data_screen.file_manager.path
        with open(self.filepath, "r") as f1:
            with open("./sampledata/user_file.csv", "r") as f2:
                for line1, line2 in zip(f1, f2):
                    self.assertEqual(line1, line2)


class FormatofHistoryFileIsGood(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test_Format(self):
        self.netflix_new_data_screen = self.app.screen_manager.get_screen(
            "Netflix_New_Data_Screen"
        )
        self.netflix_new_data_screen.getFile(None)
        self.filepath = self.netflix_new_data_screen.history_file_path
        with open(self.filepath, "r") as f1:
            with open("./sampledata/data_with_actress.csv", "r") as f2:
                for line1, line2 in zip(f1, f2):
                    self.assertEqual(line1, line2)
