import pandas as pd
import requests
import time
from app.backend.netflixupdatedata import NetflixUpdateData as UD


class NetflixLoadingScreen:
    def __init__(self):
        self.finishedLoading = 0

    def TimeTest(self):
        x = ["Avengers", "John+Wick", "Alice+in+Borderlands", "The+Matrix", "Baywatch"]
        start = time.time()
        for i in range(5):
            y = requests.get(
                f"https://api.themoviedb.org/3/search/movie?api_key=2fd4f8fec4042fda3466a92e18309708&query={x[i]}")
        end = time.time()
        return (end - start) / 5

    def Time(self):
        self.update = UD("app/backend/files/test.csv")
        time = self.TimeTest()
        df = pd.read_csv(self.update.csvFile)
        size = len(df)
        return time, size

    def StartUpdatingData(self):
        self.update.formatUserData()
        self.finishedLoading = 1
