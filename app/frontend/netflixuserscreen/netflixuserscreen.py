import pandas as pd
import os

from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.widget import MDWidget
from kivy.config import Config
from requests.exceptions import ConnectionError

Config.set('kivy', 'exit_on_escape', '0')
from app.backend.netflix.charts import NetflixCharts
from app.backend.netflix.main_screen import NetflixMainScreen
from app.backend.netflix.top_lists import NetflixTopLists
from app.backend.netflix.tmdb_api import single_movie_search
from libs.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

user_file_last = os.path.abspath("app/backend/netflix/database/last_file.csv")
netflix_final_data = os.path.abspath("app/backend/netflix/database/final_data.csv")
last_upload = os.path.abspath("app/backend/netflix/database/last_upload.csv")


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
        try:
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
                    ],
                )
            self.__dialog.open()
        except ConnectionError:
            pass

class NetflixUserScreen(MDScreen):
    widgets = []

    def generate_screens(self):
        self.__generate_main_screen()
        self.__generate_charts()
        self.__generate_history("")
        self.__generate_top_lists()

    def __generate_main_screen(self):
        netflix_main_screen = NetflixMainScreen()
        self.manager.get_screen("netflixuserscreen").ids.total_movies.text = str(
            netflix_main_screen.count_movies()
        )
        self.manager.get_screen("netflixuserscreen").ids.total_series.text = str(
            netflix_main_screen.count_series()
        )

    def __generate_charts(self):
        charts = NetflixCharts()
        charts_screen = self.manager.get_screen("netflixuserscreen").ids

        self.__charts_list = [
            charts_screen.genres_chart,
            charts_screen.movies_series_chart,
            charts_screen.years_chart,
            charts_screen.time_at_series
        ]
        self.__current_chart = 0

        charts_screen.genres_chart.add_widget(
            FigureCanvasKivyAgg(charts.genres_chart())
        )
        charts_screen.movies_series_chart.add_widget(
            FigureCanvasKivyAgg(charts.series_vs_film_chart())
        )
        charts_screen.years_chart.add_widget(
            FigureCanvasKivyAgg(charts.favourite_year())
        )
        charts_screen.time_at_series.add_widget(
            FigureCanvasKivyAgg(charts.time_at_series())
        )

    def change_chart(self, *args):
        self.__charts_list[self.__current_chart].size_hint_y = 0.0001
        self.__current_chart = (self.__current_chart + 1) % len(self.__charts_list)
        self.__charts_list[self.__current_chart].size_hint_y = 1

    def search_history(self):
        text = self.manager.get_screen("netflixuserscreen").ids.textfield.text
        self.__generate_history(text)

    def __generate_history(self, text):
        try:
            df = pd.read_csv(last_upload)
        except pd.errors.EmptyDataError:
            df = pd.read_csv(user_file_last)
        if text.strip() == "":
            data_array = df.to_dict("records")
        else:
            data_array = df[df["Title"].str.contains(text, case=False)]
            data_array = data_array.to_dict("records")

        children = self.manager.get_screen("netflixuserscreen").ids.historylist.children
        excess_children = children[:-4]
        for child in excess_children:
            self.manager.get_screen("netflixuserscreen").ids.historylist.remove_widget(
                child
            )
        self.__generate_history_list(data_array)

    def __generate_history_list(self, data_array):
        root = self.manager.get_screen("netflixuserscreen").ids.historylist
        row, possible = 0, 100
        while row < min(len(data_array), possible):
            if data_array[row]["Title"].find("_") != -1:
                possible, row = possible + 1, row + 1
                continue
            listelement = CustomButton(size_hint_y=None)
            listelement.ids.one_text.text = data_array[row]["Title"]
            try:
                listelement.ids.two_text.text = data_array[row]["Date"]
            except KeyError:
                listelement.ids.two_text.text = data_array[row]["Start Time"][:10]
            row += 1
            root.add_widget(listelement)
            space = MDWidget(height=self.height * 0.05)
            root.add_widget(space)
        root.bind(minimum_height=root.setter("height"))

    def __generate_top_lists(self):
        self.widgets = []
        for widget in self.manager.get_screen("netflixuserscreen").ids.netflixtoplistscreen.children:
            self.widgets.append(widget)
        self.widgets.reverse()

        netflix_top_lists = NetflixTopLists()
        custom_list = self.manager.get_screen(
            "netflixuserscreen"
        ).ids.netflixtoplistscreen

        index = 1
        for person, titles in netflix_top_lists.top_actors.iterrows():
            list_item = CustomThreeLineListItem(
                font_style="H6",
                text_color="#E0E0E0",
                secondary_text_color="#A7F500",
                text=f"{index}. {person}",
                secondary_text=f"{titles[0]} appearances in history",
                tertiary_text=", ".join(titles[1]),
            )
            index += 1
            custom_list.add_widget(list_item, 8)

        index = 1
        for genre, number in netflix_top_lists.top_genres.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {genre}",
                secondary_text=f"{number[0]} movies/series"
            )
            index += 1
            custom_list.add_widget(list_item, 6)

        index = 1
        for serie, hours in netflix_top_lists.top_series.iterrows():
            if type(hours[1]) != int:
                time = hours[1].split(':')
            list_item = CustomTwoLineListItem(
                text=f"{index}. {hours[0]}",
                secondary_text=f"Number of episodes: {hours[1]}" if type(
                    hours[1]) == int else f"{time[0]}h {time[1]}m {time[2]}s"
            )
            index += 1
            custom_list.add_widget(list_item, 4)

        index = 1
        for _, title in netflix_top_lists.most_popular_watched.iterrows():
            list_item = CustomOneLineListItem(
                text=f"{index}. {title[0]}"
            )
            index += 1
            custom_list.add_widget(list_item, 2)

        index = 1
        for date, titles in netflix_top_lists.top_day_watched.iterrows():
            list_item = CustomThreeLineListItem(
                font_style="H6",
                text_color="#E0E0E0",
                secondary_text_color="#A7F500",
                text=f"{index}. {date}",
                secondary_text=f"{titles[0]} titles",
                tertiary_text=", ".join(
                    [f"{item} - {count}" for item, count in sorted(titles[1].items(), key=lambda x: -int(x[1]))]),
            )
            index += 1
            custom_list.add_widget(list_item, 0)

    def back_to_main_screen(self):
        self.parent.current = "mainscreen"
        with open(netflix_final_data, "w", newline="") as csv_file:
            csv_file.truncate()
        self.manager.get_screen("netflixuserscreen").ids.genres_chart.clear_widgets()
        self.manager.get_screen("netflixuserscreen").ids.movies_series_chart.clear_widgets()
        self.manager.get_screen("netflixuserscreen").ids.years_chart.clear_widgets()
        self.manager.get_screen("netflixuserscreen").ids.time_at_series.clear_widgets()
        self.manager.get_screen("netflixuserscreen").ids.netflixtoplistscreen.clear_widgets()
        self.parent.get_screen(
            "netflixnewdatascreen"
        ).ids.filemanagericon.icon = "folder-plus"
        self.parent.get_screen(
            "netflixnewdatascreen"
        ).ids.fileadd.text = "Add your file"
        self.parent.get_screen(
            "netflixnewdatascreen"
        ).ids.filename.text = "Your file path"
        custom_list = self.manager.get_screen(
            "netflixuserscreen"
        ).ids.netflixtoplistscreen
        for widget in self.widgets:
            custom_list.add_widget(widget)
