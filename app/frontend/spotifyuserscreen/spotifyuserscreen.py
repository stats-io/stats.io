from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
import pandas as pd


class CustomTwoLineListItem(TwoLineListItem):
    pass


class SpotifyUserScreen(MDScreen):
    def generate_screens(self):
        self.__generate_top_lists()

    def __generate_top_lists(self):
        data_array = pd.read_csv("app/backend/files/Spotify/top_tracks.csv")
        custom_list = self.manager.get_screen(
            "spotifyuserscreen"
        ).ids.spotifytoplistscreen

        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item)
