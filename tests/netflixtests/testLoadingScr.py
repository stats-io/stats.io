import unittest
import pandas as pd
import time
import sys

sys.path.insert(0, "..")
from aplication.app import setUp


class LoadingisFinished(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testisFinished(self):
        start_time = time.time()
        self.netflix_loading = self.app.screen_manager.get_screen(
            "Netflix_Loading_Screen"
        )
        self.netflix_loading.startUpdatingData(None)
        if self.netflix_loading.finished_loading == 1:
            end_time = time.time()
        else:
            end_time = time.time() * 20
        duration = end_time - start_time
        self.assertLess(duration, 240)


class UpdateFileisvalid(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testUpdatevalid(self):
        self.netflix_loading = self.app.screen_manager.get_screen(
            "Netflix_Loading_Screen"
        )
        self.netflix_loading.startUpdatingData(None)
        self.file = self.netflix_loading.update
        self.testfile = pd.read_csv("./sampledata/data_with_actress.csv")
        self.assertEqual(self.testfile.equals(self.file), True)


class GoToNetflixMainScreen(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def test(self):
        self.netflix_loading = self.app.screen_manager.get_screen(
            "Netflix_Loading_Screen"
        )
        self.netflix_loading.startUpdatingData(None)
        self.app.screen_manager.get_screen("Netflix_Loading_Screen").NetflixMainScreen(
            None
        )
        current_screen = self.app.screen_manager.current
        self.assertEqual(
            self.netflix_loading.finished_loading == 1,
            current_screen == "Netflix_Main_Screen",
        )
