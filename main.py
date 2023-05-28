import os
import platform
from kivy.lang import Builder
from kivy.config import Config
from kivy import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from jnius import autoclass

from app.frontend.mainscreen.mainscreen import MainScreen
from app.frontend.netflixloadingscreen.netflixloadingscreen import NetflixLoadingScreen
from app.frontend.netflixnewdatascreen.netflixnewdatascreen import NetflixNewDataScreen
from app.frontend.netflixuserscreen.netflixuserscreen import NetflixUserScreen
from app.frontend.spotifyloginscreen.spotifyloginscreen import SpotifyLoginScreen
from app.frontend.spotifynewdatascreen.spotifynewdatascreen import SpotifyNewDataScreen
from app.frontend.spotifyuserscreen.spotifyuserscreen import SpotifyUserScreen
from app.frontend.spotifyloadingscreen.spotifyloadingscreen import SpotifyLoadingScreen


Builder.load_file("main.kv")
Builder.load_file("app/frontend/mainscreen/mainscreen.kv")
Builder.load_file("app/frontend/netflixloadingscreen/netflixloadingscreen.kv")
Builder.load_file("app/frontend/netflixnewdatascreen/netflixnewdatascreen.kv")
Builder.load_file("app/frontend/netflixuserscreen/netflixuserscreen.kv")
Builder.load_file("app/frontend/spotifyloginscreen/spotifyloginscreen.kv")
Builder.load_file("app/frontend/spotifynewdatascreen/spotifynewdatascreen.kv")
Builder.load_file("app/frontend/spotifyuserscreen/spotifyuserscreen.kv")
Builder.load_file("app/frontend/spotifyloadingscreen/spotifyloadingscreen.kv")

spotify_final_data = os.path.abspath("app/backend/spotify/database/new_data.csv")
netflix_final_data = os.path.abspath("app/backend/netflix/database/final_data.csv")

if platform == "android":
    from android.permissions import request_permissions, Permission
    version = autoclass('android.os.Build$VERSION')
    android_version = version.RELEASE
    if int(android_version) >= 10:
        request_permissions([
            Permission.INTERNET,
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_MEDIA_VIDEO,
            Permission.READ_MEDIA_AUDIO
        ])
    else:
        request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])

class WindowManager(MDScreenManager):
    pass


class StatsApp(MDApp):
    def build(self):
        self.title = "stats.io"
        return WindowManager()

    def on_stop(self):
        with open(
                netflix_final_data, "w", newline=""
        ) as csv_file:
            csv_file.truncate()
        with open(
                spotify_final_data, "w", newline=""
        ) as csv_file:
            csv_file.truncate()


if __name__ == "__main__":
    StatsApp().run()
