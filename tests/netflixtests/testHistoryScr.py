import unittest
import pandas as pd
import sys

sys.path.insert(0, "..")
from aplication.app import NetflixHistoryScreen, setUp


class NetflixList(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testGenerateListFromCSV(self):
        NHS = NetflixHistoryScreen()
        NHS.loadHistory("./sampledata/data_with_genres.csv")

        with open("./sampledata/data_with_genres.csv") as file:
            reader = pd.read_csv(file)
            data = list(reader)

        all_films = []
        for i in NHS.list_of_films.children:
            all_films.append(i.text)

        for l1, l2 in zip(data, all_films):
            self.assertEqual(l1, l2)


class NetflixSearch(unittest.TestCase):
    app = setUp()
    app.screen_manager = app.build()

    def testNetflixListSearch(self):
        NHS = NetflixHistoryScreen()
        NHS.loadHistory("./sampledata/data_with_genres.csv")
        NHS.searchTitle("The")

        with open("./sampledata/expected_search_result.csv") as file:
            reader = pd.read_csv(file)
            data = list(reader)

        searched = []
        for i in NHS.list_of_films.children:
            searched.append(i.text)

        for l1, l2 in zip(data, searched):
            self.assertEqual(l1, l2)

    def testNetflixListFilter(self):
        NHS = NetflixHistoryScreen()
        NHS.loadHistory("./sampledata/data_with_genres.csv")
        NHS.searchFiltered("Drama|Crime")

        with open("./sampledata/expected_filter_result.csv") as file:
            reader = pd.read_csv(file)
            data = list(reader)

        searched = []
        for i in NHS.list_of_films.children:
            searched.append(i.text)

        for l1, l2 in zip(data, searched):
            self.assertEqual(l1, l2)
