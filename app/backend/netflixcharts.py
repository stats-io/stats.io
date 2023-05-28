import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import os

final_data = os.path.abspath("app/backend/netflix/database/final_data.csv")
last_data = os.path.abspath("app/backend/netflix/database/last_file.csv")


class NetflixCharts:
    def __init__(self, file=final_data):
        self.csv_file = self.read_csv_file(file)

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

    def _adjust_colors_candles(self, fig, ax):
        ax.set_facecolor("#080808")
        fig.patch.set_facecolor("#080808")
        ax.tick_params(colors="#E0E0E0")
        ax.spines["bottom"].set_color("#A7F500")
        ax.spines["top"].set_color("#080808")
        ax.spines["right"].set_color("#080808")
        ax.spines["left"].set_color("#A7F500")

    def format_data(self, date):
        pattern = r"(\d{1,2})/(\d{1,2})/(\d{2})"
        match = re.match(pattern, date)
        if match:
            month = match.group(1).zfill(2)
            day = match.group(2).zfill(2)
            year = "20" + match.group(3).zfill(2)
            return f"{year}-{month}-{day}"

    def dates_chart(self):
        self.data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        dates_counter = {}
        for ind, row in self.data_array.iterrows():
            dates_tmp = row["Dates"]
            dates_tmp = eval(dates_tmp)
            for dates1 in dates_tmp:
                if type(dates1) != list:
                    dates_counter[dates1] = dates_counter.get(dates1, 0) + 1
                else:
                    for date in dates1:
                        dates_counter[date] = dates_counter.get(date, 0) + 1

        dates = pd.DataFrame.from_dict(dates_counter, orient="index", columns=["value"])
        dates = dates.sort_values("value", ascending=False)
        y = dates.index
        tmp = pd.DataFrame(columns=["date"])
        is_big = 0

        for i, date in enumerate(y):
            if date[2] == "/" or date[1] == "/":
                tmp.loc[i] = self.format_data(date)
            else:
                is_big = 1
                break

        if is_big == 0:
            tmp["date"] = pd.to_datetime(tmp["date"], format="%Y-%m-%d")
            dates.index = tmp["date"]
        else:
            tmp["date"] = dates.index
            dates.index = tmp["date"]

        dates = dates.sort_values("date")
        y = dates.index
        tmp = pd.DataFrame(columns=["date"])
        for i, date in enumerate(y):
            data = str(date)
            if is_big == 0:
                tmp.loc[i] = data[0:-12]
            else:
                tmp.loc[i] = data[0:]

        dates.index = tmp["date"]
        dates = dates.groupby(dates.index).sum()
        dates.index = pd.to_datetime(dates.index, format="%d.%m.%Y")
        dates = dates.resample("6M").sum()
        dates.index = pd.to_datetime(dates.index, format="%d.%m.%Y").strftime("%Y-%m")
        fig, ax = plt.subplots(figsize=(10, 5))
        dates.plot(kind="bar", ax=ax, color="#A7F500", legend=False)
        plt.xticks(fontsize=8)
        plt.xticks(rotation=0)
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.set_title(
            "Number of watched shows",
            fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
        )
        self._adjust_colors_candles(fig, ax)
        return plt.gcf()

    def series_vs_film_chart(self):
        film_counter = len(self.data_array[self.data_array["type"] == "film"])
        series_counter = len(self.data_array[self.data_array["type"] == "series"])
        sizes = [film_counter, series_counter]
        colors = ["#A7F500", "#E0E0E0"]
        fig, ax = plt.subplots()
        pie_wedge_collection, texts, autotexts = ax.pie(
            sizes,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            textprops={
                "color": "#080808",
                "fontsize": 8,
                "horizontalalignment": "center",
                "verticalalignment": "center",
            },
        )
        labels = ["Films", "Series"]
        leg = ax.legend(
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.1),
            fontsize=8,
            ncol=2,
            edgecolor="#080808",
        )
        fig.patch.set_facecolor("#080808")
        for text in leg.get_texts():
            text.set_color("#E0E0E0")
        ax.set_title(
            "Series to films ratio",
            fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
        )
        leg._legend_title_box._text.set_color("#E0E0E0")
        leg.get_frame().set_facecolor("#080808")
        plt.subplots_adjust(bottom=0.5)
        return plt.gcf()

    def genres_chart(self):
        genres_counter = {}
        self.data_array = pd.read_csv(
            self.read_csv_file(final_data)
        )
        for ind, row in self.data_array.iterrows():
            genres_tmp = row["genres"]
            genres_tmp = eval(genres_tmp)
            for genre in genres_tmp:
                genres_counter[genre] = genres_counter.get(genre, 0) + 1
        genres = pd.DataFrame.from_dict(
            genres_counter, orient="index", columns=["value"]
        )
        genres = genres.sort_values("value", ascending=False)
        other_rows = genres[genres["value"] <= 3]
        other_rows = other_rows["value"].sum()
        genres = genres[genres["value"] > 3]
        other_row = pd.DataFrame({"value": [other_rows]}, index=["Others"])
        genres = pd.concat([genres, other_row])

        colors = [
            "#A7F500",
            "#C2F52B",
            "#DFF55C",
            "#F5F218",
            "#F5C118",
            "#F58B18",
            "#F55B18",
            "#F53518",
            "#F51818",
            "#E01B4F",
            "#E04F6F",
            "#E0828F",
            "#E0B5AF",
            "#E0E0CF",
            "#B5E0AF",
            "#82E082",
            "#4FE052",
            "#4FB56F",
            "#4FE0A3",
            "#4FE0CF",
            "#4FB5CF",
            "#4F82CF",
            "#4F4FCF",
            "#824FCF",
            "#B54FCF",
            "#E04FCF",
            "#E04F8F",
            "#E0B5CF",
            "#B5B5E0",
            "#8282E0",
            "#4F4FE0",
            "#666666",
        ]

        fig, ax = plt.subplots(facecolor="none")
        ax.pie(genres["value"], labels=None, colors=colors)

        ax.set_title(
            "Genres chart",
            fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
        )
        fig.patch.set_facecolor("#080808")
        ax.set_xlabel(None)
        leg = ax.legend(
            genres.index,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.1),
            fontsize=8,
            ncol=2,
            edgecolor="#080808",
        )
        for text in leg.get_texts():
            text.set_color("#E0E0E0")
        leg._legend_title_box._text.set_color("#E0E0E0")
        leg.get_frame().set_facecolor("#080808")
        plt.subplots_adjust(bottom=0.5)
        return plt.gcf()

    def favourite_year(self):
        release_year = pd.read_csv(
            self.read_csv_file(final_data)
        )
        release_year["Release Date"] = release_year["Release Date"].str.slice(0, 4)
        release_year = release_year[["title", "Release Date"]]
        years_counter = {year: 0 for year in range(2000, 2024)}
        for ind, row in release_year.iterrows():
            year = row["Release Date"]
            if type(year) is float:
                continue
            year = int(year)
            if year in years_counter.keys():
                years_counter[year] += 1
            else:
                years_counter[year] = 1
        sum_under_2000 = 0
        for key in list(years_counter.keys()):
            if key < 2000:
                sum_under_2000 += years_counter[key]
                years_counter.pop(key)
        years_counter[1999] = sum_under_2000
        years = pd.DataFrame.from_dict(years_counter, orient="index", columns=["value"])
        years = years.sort_index(axis=0)
        years = years.rename(index={1999: "<2000"})
        fig, ax = plt.subplots()
        years.plot(kind="barh", ax=ax, color="#A7F500", legend=False)
        ax.set_yticks(ax.get_yticks()[-1::-2])
        ax.set_title(
            "Most watched films from years",
            fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of films/series")

        self._adjust_colors_candles(fig, ax)
        return plt.gcf()

    def time_at_series(self):
        dataArray = pd.read_csv(
            self.read_csv_file(final_data)
        )
        if np.isnan(dataArray.iloc[0, 6]):
            dataArray = dataArray.sort_values("number_of_episodes").tail(20)
            result = dataArray[["title", "number_of_episodes"]].copy()
            result = result[result["number_of_episodes"] >= 10]
            result = result.reset_index(drop=True)
            fig, ax = plt.subplots()
            ax.barh(result["title"], result["number_of_episodes"], color="#A7F500")
            ax.set_ylabel("Tytuły")
            ax.tick_params(axis="y", labelsize=8)
            self._adjust_colors_candles(fig, ax)
            ax.set_title(
                "Most episodes watched",
                fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
            )
        else:
            dataArray = dataArray.sort_values("SumOfTime").tail(20)
            result = dataArray[["title", "SumOfTime"]].copy()
            result = result[result["SumOfTime"] >= 600]
            result = result.reset_index(drop=True)
            fig, ax = plt.subplots()
            ax.barh(result["title"], result["SumOfTime"] / 60, color="#A7F500")
            ax.set_ylabel("Tytuły")
            ax.tick_params(axis="y", labelsize=8)
            self._adjust_colors_candles(fig, ax)
            ax.set_title(
                "Most time spent shows",
                fontdict={"fontsize": 14, "color": "#E0E0E0", "weight": "bold"},
            )

        return plt.gcf()
