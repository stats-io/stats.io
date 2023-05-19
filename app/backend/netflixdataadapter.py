import numpy as np
import pandas as pd


class NetflixDataAdapter:
    def __init__(self, path):
        self.csv_file = path

    def remake_file(self):
        self.data = pd.read_csv(self.csv_file)
        if self.data.shape[1] != 2:
            self.remake_file_long()
        else:
            self.remake_file_short()

    def get_total_time(self, data):
        self.title = {}
        self.title_final = {}

        for row in data.iterrows():
            time_str = row[1][2]
            hours, minutes, seconds = map(int, time_str.split(":"))
            time_in_seconds = (hours * 60 + minutes) * 60 + seconds

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

    def film_or_series(self, data):
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

    def film_or_series_dates_short(self, data):
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
        return (
            self.film_tab,
            self.series_tab,
            self.film_tab_dates,
            self.series_tab_dates,
        )

    def get_data(self, data):
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

    def remake_file_long(self):
        self.data = pd.read_csv(self.csv_file)
        self.data = self.data.loc[self.data["Supplemental Video Type"].isna()]
        self.total_data = self.get_data(self.data)
        self.total_time = self.get_total_time(self.data)
        self.film_ep, self.series_ep = self.film_or_series(self.data)
        self.adapted_data = []
        for key, value in self.film_ep.items():
            new = {
                "title": f"{key}",
                "type": "film",
                "number_of_episodes": value,
                "SumOfTime": self.total_time[key],
                "Dates": self.total_data[key],
            }
            self.adapted_data.append(new)
        for key, value in self.series_ep.items():
            new = {
                "title": f"{key}",
                "type": "series",
                "number_of_episodes": value,
                "SumOfTime": self.total_time[key],
                "Dates": self.total_data[key],
            }
            self.adapted_data.append(new)

        self.df = pd.DataFrame(self.adapted_data)
        self.df.insert(3, "genres", value=np.nan)
        self.df.insert(4, "popularity", value=np.nan)
        self.df.insert(7, "TMBDid", value=np.nan)
        self.df.insert(8, "Release Date", value=np.nan)
        self.df.insert(5, "actress", value=np.nan)
        self.df.to_csv("app/backend/files/Netflix/adapted_data.csv", index=False)
        self.csv_file = "app/backend/files/Netflix/adapted_data.csv"

    def remake_file_short(self):
        self.data = pd.read_csv(self.csv_file)
        (
            self.film_ep,
            self.series_ep,
            self.film_dates,
            self.series_dates,
        ) = self.film_or_series_dates_short(self.data)
        self.adapted_data = []

        for key, value in self.film_ep.items():
            new = {
                "title": f"{key}",
                "type": "film",
                "number_of_episodes": value,
                "Dates": self.film_dates[key],
            }
            self.adapted_data.append(new)
        for key, value in self.series_ep.items():
            new = {
                "title": f"{key}",
                "type": "series",
                "number_of_episodes": value,
                "Dates": self.series_dates[key],
            }
            self.adapted_data.append(new)

        self.df = pd.DataFrame(self.adapted_data)
        self.df.insert(3, "genres", value=np.nan)
        self.df.insert(4, "popularity", value=np.nan)
        self.df.insert(5, "actress", value=np.nan)
        self.df.insert(6, "SumOfTime", value=np.nan)
        self.df.insert(8, "TMBDid", value=np.nan)
        self.df.insert(9, "Release Date", value=np.nan)
        self.df.to_csv("app/backend/files/Netflix/adapted_data.csv", index=False)
        self.csv_file = "app/backend/files/Netflix/adapted_data.csv"
