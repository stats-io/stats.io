import pandas as pd

class SpotifyMainScreen:

    def __init__(self):
        self.csvFile = self.ReadCSV()
        self.TotalArtists = 0
        self.TotalSongs = 0
        self.TotalTime = 0

    def ReadCSV(self):
        self.Last = "app/backend/files/Spotify/Last_Data.csv"
        self.new = "app/backend/files/Spotify/Spotify_Data.csv"
        try:
            self.DataArray = pd.read_csv(self.new)
            return self.new
        except pd.errors.EmptyDataError:
            pass
        try:
            self.DataArray = pd.read_csv(self.Last)
            return  self.Last
        except pd.errors.EmptyDataError:
            return None

    def CountArtists(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return self.DataArray['Artist'].nunique()

    def CountSongs(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return self.DataArray['Title'].nunique()

    def msConverter(self):
        ms = self.DataArray['Time'].sum()
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        seconds %= 60
        minutes %= 60
        hours %= 24

        return f"{days} dni {hours} godzin {minutes} minut {seconds} sekund"

    def CountTime(self):
        self.DataArray = pd.read_csv(self.csvFile)
        ms = self.DataArray['Time'].sum()
        return self.msConverter()

