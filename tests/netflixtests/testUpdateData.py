import unittest
import pandas as pd
import sys

sys.path.insert(0, "..")
from aplication.app import NetflixUpdateData


class FormatDataTest(unittest.TestCase):
    def test(self):
        UD = NetflixUpdateData()
        UD.csvFile = "./sampledata/adapted_data.csv"
        UD.data = pd.read_csv(UD.csvFile)
        UD.formatUserData()
        self.test_data = pd.read_csv("./sampledata/data_with_actress.csv")
        self.data = UD.data
        self.assertEqual(self.data.equals(self.test_data), True)


class LookintoTMBD(unittest.TestCase):
    def test(self):
        UD = NetflixUpdateData()
        UD.csvFile = "./sampledata/adapted_data.csv"
        UD.data = pd.read_csv(UD.csvFile)
        UD.lookintoTMBD()
        self.test_data = pd.read_csv("./sampledata/data_with_actress.csv")
        self.data = UD.data
        self.assertEqual(self.data.equals(self.test_data), True)


class LookintoLocalDb(unittest.TestCase):
    def test(self):
        UD = NetflixUpdateData()
        UD.csvFile = "./sampledata/adapted_data.csv"
        UD.data = pd.read_csv(UD.csvFile)
        UD.lookintoLocalDb()
        self.test_data = pd.read_csv("./sampledata/from_database_file.csv")
        self.data = UD.data
        self.assertEqual(self.data.equals(self.test_data), True)


class FetchintoLocalDb(unittest.TestCase):
    def test(self):
        UD = NetflixUpdateData()
        UD.csvFile = "./sampledata/data_with_actress.csv"
        UD.data = pd.read_csv(UD.csvFile)
        UD.fetchintoLocalDb()
        self.db_after = pd.read_csv("./sampledata/local_database.csv")
        self.db_test = pd.read_csv("./sampledata/local_database_after_search.csv")
        self.assertEqual(self.db_after.equals(self.db_test), True)
