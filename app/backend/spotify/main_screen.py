import pandas as pd


class SpotifyMainScreen:
    def __init__(self):
        self.csv_file = self.read_csv()
        self.total_artists = 0
        self.total_songs = 0
        self.total_time = 0

    def read_csv(self):
        self.last = "app/backend/spotify/database/last_data.csv"
        self.new = "app/backend/spotify/database/new_data.csv"
        try:
            self.data_array = pd.read_csv(self.new)
            return self.new
        except pd.errors.EmptyDataError:
            pass
        try:
            self.data_array = pd.read_csv(self.last)
            return self.last
        except pd.errors.EmptyDataError:
            return None

    def count_artists(self):
        self.data_array = pd.read_csv(self.csv_file)
        return self.data_array["Artist"].nunique()

    def count_songs(self):
        self.data_array = pd.read_csv(self.csv_file)
        return self.data_array["Title"].nunique()

    def ms_converter(self):
        ms = self.data_array["Time"].sum()
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        seconds %= 60
        minutes %= 60
        hours %= 24

        return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"

    def count_time(self):
        self.data_array = pd.read_csv(self.csv_file)
        ms = self.data_array["Time"].sum()
        return self.ms_converter()
