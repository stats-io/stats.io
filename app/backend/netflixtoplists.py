import re
import numpy as np
import pandas as pd
import os

final_data = os.path.abspath("app/backend/files/Netflix/Final_Data.csv")
last_data = os.path.abspath("app/backend/files/Netflix/LastData.csv")

class NetflixTopLists:
    def __init__(self, file=final_data):
        self.csv_file = self.read_csv_file(file)
        if self.csv_file is not None:
            self.top_actors = self.get_top_actors()
            self.top_genres = self.get_top_genres()
            self.top_series = self.get_top_series()
            self.most_popular_watched = self.get_most_popular_watched()
            self.top_day_watched = self.get_top_day_watched()

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

    def get_top_actors(self):
        self.data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        actor_counter = {}
        for ind, row in self.data_array.iterrows():
            actors = row["actress"]
            actors = eval(actors)
            for actor in actors:
                actor_counter[actor] = actor_counter.get(actor, 0) + 1
        top_actors = pd.DataFrame.from_dict(
            actor_counter, orient="index", columns=["value"]
        )
        top_actors = top_actors.sort_values("value", ascending=False).head(10)
        top_actors.insert(1, "titles", value=np.nan)

        top_actors.loc[:, ("titles")] = top_actors.loc[:, ("titles")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )

        for ind1, row1 in top_actors.iterrows():
            title = []
            for ind2, row2 in self.data_array.iterrows():
                actors = row2["actress"]
                actors = eval(actors)
                for actor in actors:
                    if actor == ind1:
                        title.append(row2["title"])
            top_actors.at[ind1, "titles"] = title
        return top_actors

    def get_top_genres(self):
        self.data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        genres_counter = {}
        for ind, row in self.data_array.iterrows():
            genres = row["genres"]
            genres = eval(genres)
            for genre in genres:
                genres_counter[genre] = genres_counter.get(genre, 0) + 1
        top_genres = pd.DataFrame.from_dict(
            genres_counter, orient="index", columns=["value"]
        )
        top_genres = top_genres.sort_values("value", ascending=False).head(10)
        top_genres.insert(1, "titles", value=np.nan)
        top_genres.loc[:, ("titles")] = top_genres.loc[:, ("titles")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )

        for ind1, row1 in top_genres.iterrows():
            title = []
            for ind2, row2 in self.data_array.iterrows():
                genres = row2["genres"]
                genres = eval(genres)
                for genre in genres:
                    if genre == ind1:
                        title.append(row2["title"])
            top_genres.at[ind1, "titles"] = title
        return top_genres

    def format_data(self, date):
        pattern = r"(\d{1,2})/(\d{1,2})/(\d{2})"
        match = re.match(pattern, date)
        if match:
            month = match.group(1).zfill(2)
            day = match.group(2).zfill(2)
            year = "20" + match.group(3).zfill(2)
            return f"{year}-{month}-{day}"

    def change_sec_to_time(self, sec):
        sec = int(sec)
        hours = sec // 3600
        minutes = (sec % 3600) // 60
        seconds = sec % 60
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

    def reverse_date(self, date):
        return date[::-1]

    def get_top_series(self):
        data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        if np.isnan(data_array.iloc[0, 6]):
            data_array = data_array.sort_values(
                "number_of_episodes", ascending=False
            ).head(10)
            result = data_array[["title", "number_of_episodes"]].copy()
            result.reset_index(inplace=True)
            result.drop("index", inplace=True, axis=1)
            return result
        else:
            data_array = data_array.sort_values("SumOfTime", ascending=False).head(10)
            result = data_array[["title", "SumOfTime"]].copy()
            result["SumOfTime"] = result["SumOfTime"].apply(
                lambda x: self.change_sec_to_time(x)
            )
            result.rename(columns={"SumOfTime": "Time (HH:MM:SS)"}, inplace=True)
            result.reset_index(inplace=True)
            result.drop("index", inplace=True, axis=1)
            return result

    def get_most_popular_watched(self):
        data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        data_array = data_array.sort_values("popularity", ascending=False).head(10)
        result = data_array[["title", "popularity"]].copy()
        result.reset_index(inplace=True)
        result.drop("index", inplace=True, axis=1)
        return result

    def get_top_day_watched(self):
        dates_counter = {}
        for ind, row in self.data_array.iterrows():
            dates = row["Dates"]
            dates = eval(dates)
            for dates1 in dates:
                if type(dates1) != list:
                    dates_counter[dates1] = dates_counter.get(dates1, 0) + 1
                else:
                    for date in dates1:
                        dates_counter[date] = dates_counter.get(date, 0) + 1
        top_dates = pd.DataFrame.from_dict(
            dates_counter, orient="index", columns=["value"]
        )
        top_dates = top_dates.sort_values("value", ascending=False).head(10)
        top_dates.insert(1, "titles", value=np.nan)

        top_dates.loc[:, ("titles")] = top_dates.loc[:, ("titles")].apply(
            lambda x: [] if pd.isna(x) else eval(x)
        )

        for ind1, row1 in top_dates.iterrows():
            title = {}
            for ind2, row2 in self.data_array.iterrows():
                dates = row2["Dates"]
                dates = eval(dates)
                for dates1 in dates:
                    if type(dates1) != list:
                        if dates1 == ind1:
                            title[row2["title"]] = title.get(row2["title"], 0) + 1
                    else:
                        for date in dates1:
                            if date == ind1:
                                title[row2["title"]] = title.get(row2["title"], 0) + 1
            top_dates.at[ind1, "titles"] = title
        y = top_dates.index
        big_csv = 0
        tmp = pd.DataFrame(columns=["date"])
        for i, date in enumerate(y):
            if date[2] == "/" or date[1] == "/":
                tmp.loc[i] = self.format_data(date)
            else:
                big_csv = 1
                break
        if big_csv == 0:
            top_dates.index = tmp["date"]
        top_dates.index = pd.to_datetime(top_dates.index, format="%Y-%m-%d").strftime(
            "%d-%m-%Y"
        )
        return top_dates
