import datetime

import numpy as np
import pandas as pd


class NetflixDataAdapter:

    def __init__(self, path):
        self.csvFile = path

    def remakeFile(self):
        self.data = pd.read_csv(self.csvFile)
        if self.data.shape[1] != 2:
            self.remakeFileLong()
        else:
            self.remakeFileShort()

    def GetTotalTime(self, data):
        self.title = {}
        self.title_final = {}
        for row in data.iterrows():
            time_str = row[1][2]
            time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
            time_in_seconds = int((time.hour * 60 + time.minute) * 60 + time.second)
            key = row[1][4]
            if key in self.title:
                self.title[key] += time_in_seconds
            else:
                self.title[key] = time_in_seconds

        for key, value in self.title.items():
            vkey = key.split(":")[0]
            if vkey in self.title_final:
                self.title_final[vkey] += self.title[key]
            else:
                self.title_final[vkey] = self.title[key]
        return self.title_final

    def FilmOrSeries(self, data):
        self.film_tab = {}
        self.series_tab = {}
        for row in data.iterrows():
            title = row[1][4]
            if ":" in title:
                self.type = "series"
                title = row[1][4].split(":")[0]
                self.series_tab[title] = self.series_tab.get(title, 0) + 1
            else:
                self.type = "film"
                self.film_tab[title] = self.film_tab.get(title, 0) + 1
        return self.film_tab, self.series_tab

    def FilmOrSeriesDatesShort(self, data):
        self.film_tab = {}
        self.series_tab = {}
        self.film_tab_dates = {}
        self.series_tab_dates = {}
        for row in data.iterrows():
            title = row[1][0]
            if ":" in title:
                self.type = "series"
                title = row[1][0].split(":")[0]
                if title in self.series_tab_dates:
                    self.series_tab_dates[title].append(row[1][1])
                else:
                    self.series_tab_dates[title] = []
                    self.series_tab_dates[title].append(row[1][1])
                self.series_tab[title] = self.series_tab.get(title, 0) + 1
            else:
                self.type = "film"
                if title in self.film_tab_dates:
                    self.film_tab_dates[title].append(row[1][1])
                else:
                    self.film_tab_dates[title] = []
                    self.film_tab_dates[title].append(row[1][1])
                self.film_tab[title] = self.film_tab.get(title, 0) + 1
        return self.film_tab, self.series_tab, self.film_tab_dates, self.series_tab_dates

    def GetData(self, data):

        self.title = {}
        for row in data.iterrows():
            title = row[1][4].split(":")[0]
            date = row[1][1].split(" ")[0]
            if title in self.title:
                self.title[title].append(date)
            else:
                self.title[title] = []
                self.title[title].append(date)
        self.title_final = {}
        for key, value in self.title.items():
            name = key.split(":")[0]
            if name in self.title_final:
                self.title_final[name].append(self.title[key])
            else:
                self.title_final[name] = []
                self.title_final[name].append(self.title[key])
        return self.title_final

    def remakeFileLong(self):
        self.data = pd.read_csv(self.csvFile)
        self.data = self.data.loc[self.data["Supplemental Video Type"].isna()]
        self.TotalData = self.GetData(self.data)
        self.TotalTime = self.GetTotalTime(self.data)
        self.film_ep, self.series_ep = self.FilmOrSeries(self.data)
        self.adapted_data = []
        for key, value in self.film_ep.items():
            new = ({"title": f"{key}", "type": "film", "number_of_episodes": value, "SumOfTime": self.TotalTime[key],
                    "Dates": self.TotalData[key]})
            self.adapted_data.append(new)
        for key, value in self.series_ep.items():
            new = ({"title": f"{key}", "type": "series", "number_of_episodes": value, "SumOfTime": self.TotalTime[key],
                    "Dates": self.TotalData[key]})
            self.adapted_data.append(new)

        self.df = pd.DataFrame(self.adapted_data)
        self.df.insert(3, "genres", value=np.nan)
        self.df.insert(4, "popularity", value=np.nan)
        self.df.insert(7, "TMBDid", value=np.nan)
        self.df.insert(8, "Release Date", value=np.nan)
        self.df.insert(5, "actress", value=np.nan)
        self.df.to_csv("./adapted_data.csv", index=False)
        self.csvFile = "./adapted_data.csv"

    def remakeFileShort(self):
        self.data = pd.read_csv(self.csvFile)
        self.film_ep, self.series_ep, self.film_dates, self.series_dates = self.FilmOrSeriesDatesShort(self.data)
        self.adapted_data = []

        for key, value in self.film_ep.items():
            new = ({"title": f"{key}", "type": "film", "number_of_episodes": value, "Dates": self.film_dates[key]})
            self.adapted_data.append(new)
        for key, value in self.series_ep.items():
            new = ({"title": f"{key}", "type": "series", "number_of_episodes": value, "Dates": self.series_dates[key]})
            self.adapted_data.append(new)

        self.df = pd.DataFrame(self.adapted_data)
        self.df.insert(3, "genres", value=np.nan)
        self.df.insert(4, "popularity", value=np.nan)
        self.df.insert(5, "actress", value=np.nan)
        self.df.insert(6, "SumOfTime", value=np.nan)
        self.df.insert(8, "TMBDid", value=np.nan)
        self.df.insert(9, "Release Date", value=np.nan)
        self.df.to_csv("./adapted_data.csv", index=False)
        self.csvFile = "./adapted_data.csv"
