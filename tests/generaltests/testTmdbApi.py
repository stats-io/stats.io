import unittest
import pandas as pd
import sys

sys.path.insert(0, "..")
from aplication.app import TMBDApi


class MovieDataUpdate(unittest.TestCase):
    def test(self):
        TMBD = TMBDApi()
        self.testdata = pd.read_csv("./sampledata/adapted_data.csv")
        TMBD.dataArray = self.testdata
        TMBD.getMovieData()
        self.data = TMBD.dataArray
        self.testdata = pd.read_csv("./sampledata/small_file_test.csv")
        self.assertEqual(self.testdata.equals(self.data), True)


class MovieGenres(unittest.TestCase):
    def test(self):
        TMBD = TMBDApi()
        self.testdata = pd.read_csv("./sampledata/small_file_test.csv")
        TMBD.dataArray = self.testdata
        TMBD.getGenres()
        self.data = TMBD.dataArray
        self.testdata = pd.read_csv("./sampledata/data_with_genres.csv")
        self.assertEqual(self.testdata.equals(self.data), True)


class MovieActors(unittest.TestCase):
    def test(self):
        TMBD = TMBDApi()
        self.testdata = pd.read_csv("./sampledata/data_with_genres.csv")
        TMBD.dataArray = self.testdata
        TMBD.getActors()
        self.data = TMBD.dataArray
        self.testdata = pd.read_csv("./sampledata/data_with_actress.csv")
        self.assertEqual(self.testdata.equals(self.data), True)
