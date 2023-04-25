import unittest
import pandas as pd
import sys

sys.path.insert(0, "..")
from aplication.app import NetflixDataAdapter


class IsAdaptedWell(unittest.TestCase):
    def test(self):
        Ad = NetflixDataAdapter()
        self.data = "./sampledata/user_file.csv"
        Ad.data = self.data
        Ad.remakeFile()
        self.filelink = Ad.csvFile
        self.testFile = pd.read_csv("./sampledata/adapted_data.csv")
        with open(self.filelink, "r") as f1:
            with open(self.testFile, "r") as f2:
                for line1, line2 in zip(f1, f2):
                    self.assertEqual(line1, line2)
