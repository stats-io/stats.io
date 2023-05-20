from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
import app.backend.tmdbapi
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


class WindowManager(MDScreenManager):
    pass


class StatsApp(MDApp):
    def build(self):
        self.title = "stats.io"
        return WindowManager()

    def on_stop(self):
        with open(
            "app/backend/files/Netflix/Final_Data.csv", "w", newline=""
        ) as csv_file:
            csv_file.truncate()
        with open(
            "app/backend/files/Spotify/Spotify_Data.csv", "w", newline=""
        ) as csv_file:
            csv_file.truncate()


if __name__ == "__main__":
    StatsApp().run()
