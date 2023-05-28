import numpy as np
import pandas as pd
import os
from collections import defaultdict

adapter_path = os.path.abspath('./app/backend/files/Netflix/adapted_data.csv')

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
        title = {}
        title_final = {}

        for row in data.iterrows():
            time_str = row[1][2]
            hours, minutes, seconds = map(int, time_str.split(":"))
            time_in_seconds = (hours * 60 + minutes) * 60 + seconds

            key = row[1][4]

            if key in title:
                title[key] += time_in_seconds
            else:
                title[key] = time_in_seconds

        for key, value in title.items():
            vkey = key.split(":")[0]
            if vkey in title_final:
                title_final[vkey] += title[key]
            else:
                title_final[vkey] = title[key]
        return title_final

    def film_or_series(self, data):
        film_tab = {}
        series_tab = {}
        for row in data.iterrows():
            title = row[1][4]
            if ":" in title:
                type = "series"
                title = row[1][4].split(":")[0]
                series_tab[title] = series_tab.get(title, 0) + 1
            else:
                type = "film"
                film_tab[title] = film_tab.get(title, 0) + 1
        return film_tab, series_tab

    def __adapt_date_format(self, date_string):
        formats = [
            '%Y-%m-%d',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y.%m.%d',
            '%m.%d.%Y',
            '%d.%m.%Y',
        ]
        for fmt in formats:
            try:
                date_series = pd.to_datetime(date_string, format=fmt)
                return date_series.strftime('%d.%m.%Y')
            except ValueError:
                pass

    def film_or_series_dates_short(self, data):
        film_tab = defaultdict(int)
        series_tab = defaultdict(int)
        film_tab_dates = defaultdict(list)
        series_tab_dates = defaultdict(list)
        for row in data.iterrows():
            title = row[1][0]
            if ":" in title:
                type = "series"
                title = row[1][0].split(":")[0]
                series_tab_dates[title].append(self.__adapt_date_format(row[1][1]))
                series_tab[title] += 1
            else:
                type = "film"
                film_tab_dates[title].append(self.__adapt_date_format(row[1][1]))
                film_tab[title] += 1
        return (
            film_tab,
            series_tab,
            film_tab_dates,
            series_tab_dates,
        )

    def get_data(self, data):
        titles = defaultdict(list)
        for row in data.iterrows():
            title = row[1][4].split(":")[0]
            date = self.__adapt_date_format(row[1][1].split(" ")[0])
            titles[title].append(date)
        return titles

    def remake_file_long(self):
        data = self.data
        data = data.loc[data["Supplemental Video Type"].isna()]
        total_data = self.get_data(data)
        total_time = self.get_total_time(data)
        film_ep, series_ep = self.film_or_series(data)
        adapted_data = []
        for key, value in film_ep.items():
            new = {
                "title": f"{key}",
                "type": "film",
                "number_of_episodes": value,
                "SumOfTime": total_time[key],
                "Dates": total_data[key],
            }
            adapted_data.append(new)
        for key, value in series_ep.items():
            new = {
                "title": f"{key}",
                "type": "series",
                "number_of_episodes": value,
                "SumOfTime": total_time[key],
                "Dates": total_data[key],
            }
            adapted_data.append(new)

        df = pd.DataFrame(adapted_data)
        df.insert(3, "genres", value=np.nan)
        df.insert(4, "popularity", value=np.nan)
        df.insert(7, "TMBDid", value=np.nan)
        df.insert(8, "Release Date", value=np.nan)
        df.insert(5, "actress", value=np.nan)
        df.to_csv(adapter_path, index=False)
        self.csv_file = adapter_path

    def remake_file_short(self):
        data = self.data
        (
            film_ep,
            series_ep,
            film_dates,
            series_dates,
        ) = self.film_or_series_dates_short(data)
        adapted_data = []

        for key, value in film_ep.items():
            new = {
                "title": f"{key}",
                "type": "film",
                "number_of_episodes": value,
                "Dates": film_dates[key],
            }
            adapted_data.append(new)
        for key, value in series_ep.items():
            new = {
                "title": f"{key}",
                "type": "series",
                "number_of_episodes": value,
                "Dates": series_dates[key],
            }
            adapted_data.append(new)

        df = pd.DataFrame(adapted_data)
        df.insert(3, "genres", value=np.nan)
        df.insert(4, "popularity", value=np.nan)
        df.insert(5, "actress", value=np.nan)
        df.insert(6, "SumOfTime", value=np.nan)
        df.insert(8, "TMBDid", value=np.nan)
        df.insert(9, "Release Date", value=np.nan)
        df.to_csv(adapter_path, index=False)
        self.csv_file = adapter_path
