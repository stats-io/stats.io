from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList
from kivymd.uix.boxlayout import MDBoxLayout
import pandas as pd
import random
import spotipy
from spotipy import SpotifyOAuth

CLIENT_ID = "fb34b1a1fb884d5794990d691867df0f"
CLIENT_SECRET = "5cbcea13936c443690e519058bd63ac5"
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


class CustomButton(MDCard):
    pass


class CustomMDLabel(MDLabel):
    pass


class CustomMDTextField(MDTextField):
    pass


class CustomMDRaisedButton(MDRaisedButton):
    pass

    
class SpotifyUserScreen(MDScreen):
    __detailed_history = False

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

        data_array = pd.read_csv("app/backend/spotify/database/top_artists.csv")
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

    def history_screen_handler(self):
        self.manager.get_screen("spotifyuserscreen").ids.scrollview.clear_widgets()
        if self.__detailed_history:
            self.manager.get_screen("spotifyuserscreen").ids.top_app_bar.title = "Change to detailed history"
            self.__custom_list = None
            self.__generate_history()
        else:
            self.manager.get_screen("spotifyuserscreen").ids.top_app_bar.title = "Change to short history"
            self.__generate_detailed_history()
        self.__detailed_history = not self.__detailed_history
            

    def __generate_history(self):
        custom_list = MDList(divider_color="#E0E0E0",divider="Full",spacing=10,padding=20)
        data_array = pd.read_csv("app/backend/spotify/database/recently_played_tracks.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomThreeLineListItem(
                text=f"{index}. {row[1]}",
                secondary_text=f"Artist: {row[2]}",
                tertiary_text=f"Played at {row[3]}",
            )
            index += 1
            custom_list.add_widget(list_item)
        self.manager.get_screen("spotifyuserscreen").ids.scrollview.add_widget(custom_list)

    def __generate_detailed_history(self):
        self.__custom_list = MDGridLayout(cols=1, padding=20, spacing=10, size_hint_y=None)
        self.__custom_list.add_widget(CustomMDLabel())
        self.__text_field = CustomMDTextField()
        self.__custom_list.add_widget(self.__text_field)
        self.__custom_list.add_widget(CustomMDRaisedButton(on_release=lambda x: self.search_history()))

        df = self.__read_file()
        data_array = df.to_dict("records")
        self.__generate_list(data_array)

        self.manager.get_screen("spotifyuserscreen").ids.scrollview.add_widget(self.__custom_list)
            
    def __read_file(self):
        try:
            df = pd.read_csv("app/backend/spotify/database/new_data.csv")
        except pd.errors.EmptyDataError:
            df = pd.read_csv("app/backend/spotify/database/last_data.csv")
        return df

    def __generate_list(self, data_array):
        for row in range(min(100, len(data_array))):
            listelement = CustomButton(size_hint_y=None, height=80)
            listelement.ids.one_text.text = data_array[row]["Title"]
            listelement.ids.two_text.text = data_array[row]["Date"]
            self.__custom_list.add_widget(listelement)
        self.__custom_list.bind(minimum_height=self.__custom_list.setter("height"))

    def search_history(self):
        df = self.__read_file()
        text = self.__text_field.text
        if text.strip() != "":
            df = df[df["Title"].str.contains(text, case=False)]
            df = df.drop_duplicates(subset=['Title'])
        data_array = df.to_dict("records")

        children = self.__custom_list.children
        excess_children = children[:-3]
        for child in excess_children:
            self.__custom_list.remove_widget(child)
        self.__generate_list(data_array)

    def __generate_top_lists(self):
        custom_list = self.manager.get_screen(
            "spotifyuserscreen"
        ).ids.spotifytoplistscreen

        data_array = pd.read_csv("app/backend/spotify/database/top_tracks.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item, 2)

        data_array = pd.read_csv("app/backend/spotify/database/top_artists.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomOneLineListItem(text=f"{index}. {row[1]}")
            index += 1
            custom_list.add_widget(list_item, 1)

        data_array = pd.read_csv("app/backend/spotify/database/recommendations.csv")
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item, 0)

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            self.parent.current = "mainscreen"
