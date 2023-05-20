from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, TwoLineListItem
import pandas as pd


class CustomOneLineListItem(OneLineListItem):
    pass


class CustomTwoLineListItem(TwoLineListItem):
    pass


class SpotifyUserScreen(MDScreen):
    def generate_screens(self):
        self.__generate_top_lists()

    def __generate_top_lists(self):
        custom_list = self.manager.get_screen(
            "spotifyuserscreen"
        ).ids.spotifytoplistscreen

        data_array = pd.read_csv("app/backend/files/Spotify/top_tracks.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item, 2)

        data_array = pd.read_csv("app/backend/files/Spotify/top_artists.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomOneLineListItem(text=f"{index}. {row[1]}")
            index += 1
            custom_list.add_widget(list_item, 1)

        data_array = pd.read_csv("app/backend/files/Spotify/recommendations.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item, 0)
