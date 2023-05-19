import time
import pandas as pd


class NetflixMainScreen:
    def __init__(self, file="app/backend/files/Netflix/Final_Data.csv"):
        self.csvFile = self.CSVFile(file)
        self.TotalMoviesWatched = 0
        self.TotalSeriesWatched = 0

    def CSVFile(self, file):
        try:
            df = pd.read_csv(file)
            return file
        except pd.errors.EmptyDataError:
            pass
        file = "app/backend/files/Netflix/LastData.csv"
        try:
            df = pd.read_csv(file)
            return file
        except pd.errors.EmptyDataError:
            return None

    def CountMovies(self):
        time.sleep(1)
        self.csvFile = self.CSVFile("app/backend/files/Netflix/Final_Data.csv")
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray["type"] == "film"])

    def CountSeries(self):
        self.csvFile = self.CSVFile("app/backend/files/Netflix/Final_Data.csv")
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray["type"] == "series"])
