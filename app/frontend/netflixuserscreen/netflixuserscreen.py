import pandas as pd

from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from app.backend.netflixcharts import NetflixCharts
from app.backend.netflixmain import NetflixMainScreen
from app.backend.netflixtoplists import NetflixTopLists
from app.backend.tmdbapi import single_movie_search
from libs.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class CustomOneLineListItem(OneLineListItem):
    pass


class CustomTwoLineListItem(TwoLineListItem):
    pass


class CustomThreeLineListItem(ThreeLineListItem):
    pass


class CustomButton(MDCard):
    __dialog = None

    def close_dialog(self, *args):
        self.__dialog.dismiss()

    def show_bigger(self, title, date_watched):
        overview, genres, actors = single_movie_search(title)

        if not self.__dialog:
            self.__dialog = MDDialog(
                title=f"{title}\n{date_watched}",
                text=f"Genres: {genres}\n\nActors: {actors}\n\nOverview: {overview}",
                md_bg_color="#E0E0E0",
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        theme_text_color="Custom",
                        text_color="#080808",
                        md_bg_color="#A7F500",
                        on_release=self.close_dialog,
                    )
                ]
            )
        self.__dialog.open()


class NetflixUserScreen(MDScreen):

    def generate_screens(self):
        self.__generate_main_screen()
        self.__generate_charts()
        self.__generate_history("")
        self.__generate_top_lists()

    def __generate_main_screen(self):
        netflix_main_screen = NetflixMainScreen()
        self.manager.get_screen("netflixuserscreen").ids.total_movies.text = str(netflix_main_screen.CountMovies())
        self.manager.get_screen("netflixuserscreen").ids.total_series.text = str(netflix_main_screen.CountSeries())

    def __generate_charts(self):
        charts = NetflixCharts()        
        charts_screen = self.manager.get_screen("netflixuserscreen").ids
        charts_screen.genres_chart.add_widget(FigureCanvasKivyAgg(charts.GenresChart()))
        charts_screen.movies_series_chart.add_widget(FigureCanvasKivyAgg(charts.SeriesvsFilmChart()))
        charts_screen.years_chart.add_widget(FigureCanvasKivyAgg(charts.Favourite_year()))
        charts_screen.watch_count_chart.add_widget(FigureCanvasKivyAgg(charts.DatesChart()))
        charts_screen.time_at_series.add_widget(FigureCanvasKivyAgg(charts.TimeAtSeries()))

    def search_history(self):
        text = self.manager.get_screen("netflixuserscreen").ids.textfield.text
        self.__generate_history(text)

    def __generate_history(self, text):
        df = pd.read_csv("app/backend/files/Netflix/test.csv")
        data_array = None
        if text.strip() == "":
            data_array = df.to_dict("records")
        else:
            data_array = df[df["Title"].str.contains(text, case=False)]
            data_array = data_array.to_dict("records")

        children = self.manager.get_screen("netflixuserscreen").ids.historylist.children
        excess_children = children[:-3]
        for child in excess_children:
            self.manager.get_screen("netflixuserscreen").ids.historylist.remove_widget(child)
        self.__generate_history_list(data_array)

    def __generate_history_list(self, data_array):
        root = self.manager.get_screen("netflixuserscreen").ids.historylist
        row, possible = 0, 100
        while row < min(len(data_array), possible):
            if data_array[row]["Title"].find("_") != -1:
                possible, row = possible + 1, row + 1
                continue
            listelement = CustomButton(size_hint_y=None, height=80)
            listelement.ids.one_text.text = data_array[row]["Title"]
            try:
                listelement.ids.two_text.text = data_array[row]["Date"]
            except KeyError:
                listelement.ids.two_text.text = data_array[row]["Start Time"][:10]
            row += 1
            root.add_widget(listelement)
        root.bind(minimum_height=root.setter("height"))

    def __generate_top_lists(self):
        netflix_top_lists = NetflixTopLists()
        custom_list = self.manager.get_screen("netflixuserscreen").ids.netflixtoplistscreen
        try:
            index = 1
            TopActors = netflix_top_lists.TopActors
            for ind1, row1 in TopActors.iterrows():
                third_text = ""
                for item in row1[1]:
                    third_text = f"{third_text} {item},"
                list_item = CustomThreeLineListItem(
                    font_style="H6",
                    text_color="#E0E0E0",
                    secondary_text_color="#A7F500",
                    text=str(index) + ". " + ind1,
                    secondary_text=str(row1[0]) + " appearances in history",
                    tertiary_text=third_text,
                )
                index += 1
                custom_list.add_widget(list_item, 8)

            index = 1
            TopGenres = netflix_top_lists.TopGenres
            for ind1, row1 in TopGenres.iterrows():
                list_item = CustomTwoLineListItem(
                    text=str(index) + ". " + ind1,
                    secondary_text=str(row1[0]) + " movies/series"
                )
                index += 1
                custom_list.add_widget(list_item, 6)

            index = 1
            TopSeries = netflix_top_lists.TopSeries
            for ind1, row1 in TopSeries.iterrows():
                second_text = ""
                if type(row1[1]) == int:
                    second_text = f"Number of episodes: {row1[1]}"
                else:
                    line = row1[1].split(":")
                    second_text = f"{line[0]} hours {line[1]} minutes {line[2]} seconds"

                list_item = CustomTwoLineListItem(
                    text=str(index) + ". " + row1[0],
                    secondary_text=second_text
                )
                index += 1
                custom_list.add_widget(list_item, 4)

            index = 1
            Mostpopular = netflix_top_lists.MostPopularWatched
            for ind1, row1 in Mostpopular.iterrows():
                list_item = CustomOneLineListItem(
                    text=str(index) + ". " + row1[0]
                )
                index += 1
                custom_list.add_widget(list_item, 2)

            index = 1
            TopDay = netflix_top_lists.TopDayWatched
            for ind1, row1 in TopDay.iterrows():
                foo = ""
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
        except AttributeError:
            def create_top_list(self):
                custom_list = self.manager.get_screen("netflixuserscreen").ids.netflixtoplistscreen
                index = 1
                for ind1, row1 in netflix_top_lists.TopActors.iterrows():
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
                for ind1, row1 in netflix_top_lists.TopGenres.iterrows():
                    list_item = CustomTwoLineListItem(
                        text=str(index) + ". " + ind1,
                        secondary_text=str(row1[0]) + " movies/series"
                    )
                    index += 1
                    custom_list.add_widget(list_item, 6)

                index = 1
                for ind1, row1 in netflix_top_lists.TopSeries.iterrows():
                    second_text = ""
                    if type(row1[1]) == int:
                        second_text = f"Number of episodes: {row1[1]}"
                    else:
                        line = row1[1].split(":")
                        second_text = f"{line[0]} hours {line[1]} minutes {line[2]} seconds"

                    list_item = CustomTwoLineListItem(
                        text=str(index) + ". " + row1[0],
                        secondary_text=second_text
                    )
                    index += 1
                    custom_list.add_widget(list_item, 4)

                index = 1
                for ind1, row1 in netflix_top_lists.MostPopularWatched.iterrows():
                    list_item = CustomOneLineListItem(
                        text=str(index) + ". " + row1[0]
                    )
                    index += 1
                    custom_list.add_widget(list_item, 2)

                index = 1
                for ind1, row1 in netflix_top_lists.TopDayWatched.iterrows():
                    foo = ""
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
