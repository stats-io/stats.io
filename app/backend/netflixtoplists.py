from datetime import datetime

import numpy as np
import pandas as pd


class NetflixTopLists:

    def __init__(self, file="app/backend/files/BigFile.csv"):
        self.csvFile = file
        self.TopActors = self.TopActors()
        self.TopGenres = self.TopGenres()
        self.TopSeries = self.TopSeries()
        self.MostPopularWatched = self.MostPopularWatched()
        self.TopDayWatched = self.TopDayWatched()

    def Visualize(self):
        print(self.TopActors)
        print(self.TopGenres)
        print(self.TopSeries)
        print(self.MostPopularWatched)
        print(self.TopDayWatched)

    def TopActors(self):
        self.DataArray = pd.read_csv(self.csvFile)
        actor_counter = {}
        for ind, row in self.DataArray.iterrows():
            actors = row["actress"]
            actors = eval(actors)
            for actor in actors:
                actor_counter[actor] = actor_counter.get(actor, 0) + 1
        Actors = pd.DataFrame.from_dict(actor_counter, orient="index", columns=["value"])
        Actors = Actors.sort_values("value", ascending=False).head(10)
        Actors.insert(1, "titles", value=np.nan)

        Actors.loc[:, ("titles")] = Actors.loc[:, ("titles")].apply(lambda x: [] if pd.isna(x) else eval(x))

        for ind1, row1 in Actors.iterrows():
            title = []
            for ind2, row2 in self.DataArray.iterrows():
                actors = row2["actress"]
                actors = eval(actors)
                for actor in actors:
                    if actor == ind1:
                        title.append(row2["title"])
            Actors.at[ind1, "titles"] = title
        return Actors

    def TopGenres(self):
        genres_counter = {}
        for ind, row in self.DataArray.iterrows():
            genres = row["genres"]
            genres = eval(genres)
            for genre in genres:
                genres_counter[genre] = genres_counter.get(genre, 0) + 1
        Genres = pd.DataFrame.from_dict(genres_counter, orient="index", columns=["value"])
        Genres = Genres.sort_values("value", ascending=False).head(10)
        Genres.insert(1, "titles", value=np.nan)
        Genres.loc[:, ("titles")] = Genres.loc[:, ("titles")].apply(lambda x: [] if pd.isna(x) else eval(x))

        for ind1, row1 in Genres.iterrows():
            title = []
            for ind2, row2 in self.DataArray.iterrows():
                genres = row2["genres"]
                genres = eval(genres)
                for genre in genres:
                    if genre == ind1:
                        title.append(row2["title"])
            Genres.at[ind1, "titles"] = title
        return Genres

    def change_sec_to_time(self, sec):
        sec = int(sec)
        hours = sec // 3600
        minutes = (sec % 3600) // 60
        seconds = sec % 60
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

    def TopSeries(self):
        DataArray = pd.read_csv(self.csvFile)
        if np.isnan(DataArray.iloc[0, 6]):
            DataArray = DataArray.sort_values("number_of_episodes", ascending=False).head(10)
            Result = DataArray[["title", "number_of_episodes"]].copy()
            Result.reset_index(inplace=True)
            Result.drop("index", inplace=True, axis=1)
            return Result
        else:
            DataArray = DataArray.sort_values("SumOfTime", ascending=False).head(10)
            Result = DataArray[["title", "SumOfTime"]].copy()
            Result["SumOfTime"] = Result["SumOfTime"].apply(lambda x: self.change_sec_to_time(x))
            Result.rename(columns={"SumOfTime": "Time (HH:MM:SS)"}, inplace=True)
            Result.reset_index(inplace=True)
            Result.drop("index", inplace=True, axis=1)
            return Result

    def MostPopularWatched(self):
        DataArray = pd.read_csv(self.csvFile)
        DataArray = DataArray.sort_values("popularity", ascending=False).head(10)
        Result = DataArray[["title", "popularity"]].copy()
        Result.reset_index(inplace=True)
        Result.drop("index", inplace=True, axis=1)
        return Result

    def TopDayWatched(self):
        dates_counter = {}
        for ind, row in self.DataArray.iterrows():
            dates = row["Dates"]
            dates = eval(dates)
            for dates1 in dates:
                if type(dates1) != list:
                    dates_counter[dates1] = dates_counter.get(dates1, 0) + 1
                else:
                    for date in dates1:
                        dates_counter[date] = dates_counter.get(date, 0) + 1
        Dates = pd.DataFrame.from_dict(dates_counter, orient="index", columns=["value"])
        Dates = Dates.sort_values("value", ascending=False).head(10)
        Dates.insert(1, "titles", value=np.nan)

        Dates.loc[:, ("titles")] = Dates.loc[:, ("titles")].apply(lambda x: [] if pd.isna(x) else eval(x))

        for ind1, row1 in Dates.iterrows():
            title = {}
            for ind2, row2 in self.DataArray.iterrows():
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
            Dates.at[ind1, "titles"] = title
        y = Dates.index
        BigCsv = 0
        tmp = pd.DataFrame(columns=["date"])
        for i, date in enumerate(y):
            try:
                date_obj = datetime.strptime(date, "%m/%d/%y")
                tmp.loc[i] = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                BigCsv = 1
                break
        if BigCsv == 0:
            Dates.index = tmp["date"]
        return Dates
