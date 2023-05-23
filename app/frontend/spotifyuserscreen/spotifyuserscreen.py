from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.card import MDCard
import pandas as pd
import random
import spotipy
from spotipy import SpotifyOAuth

CLIENT_ID = "fb34b1a1fb884d5794990d691867df0f"
CLIENT_SECRET = "185c998c2b0449378b992a237cc418ea"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-read-recently-played user-top-read"




class CustomOneLineListItem(OneLineListItem):
    pass


class CustomTwoLineListItem(TwoLineListItem):
    pass


class CustomThreeLineListItem(ThreeLineListItem):
    pass


class CustomMDCard(MDCard):
    pass


class SpotifyUserScreen(MDScreen):
    def generate_screens(self):
        self.__generate_main_screen()
        self.__generate_history()
        self.__generate_top_lists()

    def __generate_main_screen(self):
        screen = self.manager.get_screen("spotifyuserscreen").ids.spotifymainscreen

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=SCOPE,
            )
        )

        data_array = pd.read_csv("app/backend/files/Spotify/top_artists.csv")
        number_of_lines = len(data_array)
        number_of_random_artist = random.randint(0, number_of_lines - 1)
        artist = data_array.iloc[number_of_random_artist]
        artist_name = artist["Artist"]
        search = sp.search(q=f"{artist_name}", type="artist")
        artist_id = search["artists"]["items"][0]["id"]
        results = sp.recommendations(limit=6, seed_artists=[artist_id])

        for track in results["tracks"]:
            card = CustomMDCard(pos_hint={"center_x": 0.5})
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            url = track["album"]["images"][0]["url"]
            card.ids.title_name.text = f"Title:  {track_name}"
            card.ids.artist_name.text = f"Artist: {artist_name}"
            card.ids.image_url.source = url
            screen.add_widget(card)

    def __generate_history(self):
        custom_list = self.manager.get_screen(
            "spotifyuserscreen"
        ).ids.spotifyhistoryscreen

        data_array = pd.read_csv("app/backend/files/Spotify/recently_played_tracks.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomThreeLineListItem(
                text=f"{index}. {row[1]}",
                secondary_text=f"Artist: {row[2]}",
                tertiary_text=f"Played at {row[3]}",
            )
            index += 1
            custom_list.add_widget(list_item)

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
