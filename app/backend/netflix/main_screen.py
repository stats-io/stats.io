import time
import pandas as pd
import os

final_data = os.path.abspath("app/backend/netflix/database/final_data.csv")
last_data = os.path.abspath("app/backend/netflix/database/last_file.csv")


class NetflixMainScreen:
    def __init__(self, file=final_data):
        self.csv_file = self.read_csv_file(file)
        self.total_movies_watched = 0
        self.total_series_watched = 0

    def read_csv_file(self, file):
        try:
            df = pd.read_csv(file)
            return file
        except pd.errors.EmptyDataError:
            pass
        file = last_data
        try:
            df = pd.read_csv(file)
            return file
        except pd.errors.EmptyDataError:
            return None

    def count_movies(self):
        time.sleep(1)
        self.csv_file = self.read_csv_file(final_data)
        self.data_array = pd.read_csv(self.csv_file)
        return len(self.data_array[self.data_array["type"] == "film"])

    def count_series(self):
        self.csv_file = self.read_csv_file(final_data)
        self.data_array = pd.read_csv(self.csv_file)
        return len(self.data_array[self.data_array["type"] == "series"])
