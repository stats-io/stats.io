import pandas as pd
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.screen import MDScreen

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

    def generate_history(self):
        df = pd.read_csv("app/backend/files/BigFile.csv")
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
            list_item = CustomOneLineListItem(
                text=str(index) + ". " + ind1
            )
            index += 1
            custom_list.add_widget(list_item, 8)

        index = 1
        for ind1, row1 in self.netflix_top_lists.TopGenres.iterrows():
            list_item = CustomOneLineListItem(
                text=str(index) + ". " + ind1
            )
            index += 1
            custom_list.add_widget(list_item, 6)

        index = 1
        for ind1, row1 in self.netflix_top_lists.TopSeries.iterrows():
            list_item = CustomOneLineListItem(
                text=str(index) + ". " + row1[0]
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
            print()
            list_item = CustomOneLineListItem(
                text=str(index) + ". " + str(row1)
            )
            index += 1
            custom_list.add_widget(list_item, 0)
