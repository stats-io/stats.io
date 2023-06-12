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
import pandas as pd
import random
import spotipy
import os
from spotipy import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE

new_data = os.path.abspath("app/backend/spotify/database/new_data.csv")
last_data = os.path.abspath("app/backend/spotify/database/last_data.csv")
recently_played_data = os.path.abspath("app/backend/spotify/database/recently_played_tracks.csv")
top_tracks_data = os.path.abspath("app/backend/spotify/database/top_tracks.csv")
top_artists_data = os.path.abspath("app/backend/spotify/database/top_artists.csv")
recommendations_data = os.path.abspath("app/backend/spotify/database/recommendations.csv")


class CustomOneLineListItem(OneLineListItem):
    pass


class CustomMoreListItem(OneLineListItem):
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

        data_array = pd.read_csv(top_artists_data)
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
        check = False
        if self.__detailed_history:
            self.manager.get_screen("spotifyuserscreen").ids.scrollview.clear_widgets()
            self.manager.get_screen("spotifyuserscreen").ids.top_app_bar.title = "Change to detailed history"
            self.__custom_list = None
            self.__generate_history()
            check = True
        else:
            try:
                df = self.__read_file()
                self.manager.get_screen("spotifyuserscreen").ids.scrollview.clear_widgets()
                self.manager.get_screen("spotifyuserscreen").ids.top_app_bar.title = "Change to short history"
                self.__generate_detailed_history()
                check = True
            except pd.errors.EmptyDataError:
                pass

        if check:
            self.__detailed_history = not self.__detailed_history

    def __generate_history(self):
        custom_list = MDList(divider_color="#E0E0E0",divider="Full",spacing=10,padding=20)
        data_array = pd.read_csv(recently_played_data)
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
        self.count = 1
        self.manager.get_screen("spotifyuserscreen").ids.scrollview.add_widget(self.__custom_list)
            
    def __read_file(self):
        try:
            df = pd.read_csv(new_data)
        except pd.errors.EmptyDataError:
            df = pd.read_csv(last_data)
        return df

    def __generate_list(self, data_array):
        for row in range(min(100, len(data_array))):
            listelement = CustomTwoLineListItem(
                text=data_array[row]["Title"],
                secondary_text=data_array[row]["Date"]
            )
            self.__custom_list.add_widget(listelement)
        self.__custom_list.bind(minimum_height=self.__custom_list.setter("height"))
        listelement = CustomMoreListItem(
            text="More"
        )
        listelement.bind(on_release=self.__add_more_tracks)
        self.__custom_list.add_widget(listelement)

    def __add_more_tracks(self, instance):
        parent = instance.parent
        parent.remove_widget(instance)
        df = self.__read_file()
        data_array = df.to_dict("records")
        for row in range(min(100, len(data_array))):
            if row + 100 * self.count < len(data_array):
                listelement = CustomTwoLineListItem(
                    text=data_array[row + 100 * self.count]["Title"],
                    secondary_text=data_array[row + 100 * self.count]["Date"]
                )
                self.__custom_list.add_widget(listelement)
        self.__custom_list.bind(minimum_height=self.__custom_list.setter("height"))
        listelement = CustomMoreListItem(
            text="More"
        )
        listelement.bind(on_release=self.__add_more_tracks)
        self.count += 1
        self.__custom_list.add_widget(listelement)

    def __generate_top_lists(self):
        custom_list = self.manager.get_screen(
            "spotifyuserscreen"
        ).ids.spotifytoplistscreen

        data_array = pd.read_csv(top_tracks_data)
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomTwoLineListItem(
                text=f"{index}. {row[1]}", secondary_text=f"Artist: {row[2]}"
            )
            index += 1
            custom_list.add_widget(list_item, 2)

        data_array = pd.read_csv(top_artists_data)
        index = 1
        for i, row in data_array.iterrows():
            list_item = CustomOneLineListItem(text=f"{index}. {row[1]}")
            index += 1
            custom_list.add_widget(list_item, 1)

        data_array = pd.read_csv(recommendations_data)
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
