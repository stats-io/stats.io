import pandas as pd
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.screen import MDScreen
import os
from app.backend.netflixcharts import NetflixCharts
from app.backend.netflixmain import NetflixMainScreen
from app.backend.netflixtoplists import NetflixTopLists


class CustomOneLineListItem(OneLineListItem):
    pass


class CustomTwoLineListItem(TwoLineListItem):
    pass


class CustomThreeLineListItem(ThreeLineListItem):
    pass


class NetflixUserScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.netflix_main_screen = NetflixMainScreen()
        self.netflix_top_lists = NetflixTopLists()
        self.charts = NetflixCharts()

    def generate_charts(self):
        self.manager.get_screen("netflixuserscreen").ids.total_movies.text = str(self.netflix_main_screen.CountMovies())
        self.manager.get_screen("netflixuserscreen").ids.total_series.text = str(self.netflix_main_screen.CountSeries())
        charts_screen = self.manager.get_screen("netflixuserscreen").ids
        charts_screen.genres_chart.add_widget(FigureCanvasKivyAgg(self.charts.GenresChart()))
        charts_screen.movies_series_chart.add_widget(FigureCanvasKivyAgg(self.charts.SeriesvsFilmChart()))
        charts_screen.years_chart.add_widget(FigureCanvasKivyAgg(self.charts.Favourite_year()))
        charts_screen.watch_count_chart.add_widget(FigureCanvasKivyAgg(self.charts.DatesChart()))
        charts_screen.time_at_series.add_widget(FigureCanvasKivyAgg(self.charts.TimeAtSeries()))

        self.generate_history()
        self.create_top_list()

    def CSVFile(self, file):
        f = "app/backend/files"
        try:
            df = pd.read_csv(file)
            test = 1
            return file
        except pd.errors.EmptyDataError:
            test = 0

        if test == 0:
            files = [f"{f}/LastSmallData.csv", f"{f}/LastBigData.csv"]
            latest_file = max(files, key=os.path.getmtime)
            file = latest_file
            try:
                df = pd.read_csv(file)

            except pd.errors.EmptyDataError:
                if latest_file == f"{f}/LastBigData.csv":
                    file = f"{f}/LastSmallData.csv"
                else:
                    file = f"{f}/LastBigData.csv"
        return file

    def generate_history(self):
        df = pd.read_csv(self.CSVFile("app/backend/files/Final_Data.csv"))
        data_array = df.to_dict("records")
        self.create_list(data_array)

    def create_list(self, data_array):
        lista = self.manager.get_screen("netflixuserscreen").ids.netflixhistoryscreen
        for row in range(len(data_array)):
            third = ", ".join(
                list(set(data_array[row]["Dates"].replace("[", "").replace("]", "").replace("'", "").split(", "))))
            lista.add_widget(
                CustomThreeLineListItem(
                    text=data_array[row]["title"],
                    secondary_text=data_array[row]["genres"].replace("[", "").replace("]", "").replace("'", ""),
                    tertiary_text=third,
                )
            )

    def create_top_list(self):
        custom_list = self.manager.get_screen("netflixuserscreen").ids.netflixtoplistscreen
        index = 1
        for ind1, row1 in self.netflix_top_lists.TopActors.iterrows():
            third_text = ""
            for item in row1[1]:
                third_text = f"{third_text} {item},"
            list_item = CustomThreeLineListItem(
                font_style="H6",
                text_color="#E0E0E0",
                secondary_text_color="#A7F500",
                text=str(index) + ". " + ind1,
                secondary_text=str(row1[0]) + " appearances in history",
                tertiary_text=third_text
            )
            index += 1
            custom_list.add_widget(list_item, 8)

        index = 1
        for ind1, row1 in self.netflix_top_lists.TopGenres.iterrows():
            list_item = CustomTwoLineListItem(
                text=str(index) + ". " + ind1,
                secondary_text=str(row1[0]) + " movies/series"
            )
            index += 1
            custom_list.add_widget(list_item, 6)

        index = 1
        for ind1, row1 in self.netflix_top_lists.TopSeries.iterrows():
            second_text = ""
            if type(row1[1]) == int:
                second_text = f"Number of episodes: {row1[1]}"
            else:
                line = row1[1].split(':')
                second_text = f"{line[0]} hours {line[1]} minutes {line[2]} seconds"

            list_item = CustomTwoLineListItem(
                text=str(index) + ". " + row1[0],
                secondary_text=second_text
            )
            index += 1
            custom_list.add_widget(list_item, 4)

        index = 1
        for ind1, row1 in self.netflix_top_lists.MostPopularWatched.iterrows():
            list_item = CustomOneLineListItem(
                text=str(index) + ". " + row1[0]
            )
            index += 1
            custom_list.add_widget(list_item, 2)

        index = 1
        for ind1, row1 in self.netflix_top_lists.TopDayWatched.iterrows():
            foo=""
            for item, count in row1[1].items():
                foo = f"{foo} {item} - {count},"
            foo = foo[:-1]

            list_item = CustomThreeLineListItem(
                font_style="H6",
                text_color="#E0E0E0",
                secondary_text_color="#A7F500",
                text=str(index) + ". " + str(ind1),
                secondary_text=str(row1[0]) + " titles",
                tertiary_text=foo
            )
            index += 1
            custom_list.add_widget(list_item, 0)
