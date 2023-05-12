import pandas as pd

class NetflixMainScreen:

    def __init__(self,file = 'app/backend/BigFile.csv'):
        self.csvFile = file
        self.TotalMoviesWatched = self.CountMovies()
        self.TotalSeriesWatched = self.CountSeries()

    def CountMovies(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray['type'] == 'film'])

    def CountSeries(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray['type'] == 'series'])
