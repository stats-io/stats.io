import pandas as pd
import requests
import time
from app.backend.netflixupdatedata import NetflixUpdateData as UpdateData


class NetflixLoadingScreen:
    def __init__(self):
        self.finishedLoading = 0

    def __test_time_on_sample(self):
        url = "https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query="
        movies = ["Avengers", "John+Wick", "Alice+in+Borderlands", "The+Matrix", "Baywatch", "Narcos"]
        start = time.time()
        [requests.get(f"{url}{movie}") for movie in movies]
        return (time.time() - start) / len(movies)

    def get_estimated_time(self, file_path):
        self.update = UpdateData("app/backend/files/Netflix/test.csv")
        return [self.__test_time_on_sample(), len(pd.read_csv(self.update.csvFile))]

    def start_processing_data(self):
        self.update.formatUserData()
        self.finishedLoading = 1
