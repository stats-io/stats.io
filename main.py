from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from app.frontend.mainscreen.mainscreen import MainScreen
from app.frontend.netflixloadingscreen.netflixloadingscreen import NetflixLoadingScreen
from app.frontend.netflixnewdatascreen.netflixnewdatascreen import NetflixNewDataScreen
from app.frontend.netflixuserscreen.netflixuserscreen import NetflixUserScreen

Builder.load_file("main.kv")
Builder.load_file("app/frontend/mainscreen/mainscreen.kv")
Builder.load_file("app/frontend/netflixloadingscreen/netflixloadingscreen.kv")
Builder.load_file("app/frontend/netflixnewdatascreen/netflixnewdatascreen.kv")
Builder.load_file("app/frontend/netflixuserscreen/netflixuserscreen.kv")


class WindowManager(MDScreenManager):
    pass


class StatsApp(MDApp):
    def build(self):
        self.title = "stats.io"
        return WindowManager()

    def on_stop(self):
        with open('app/backend/files/Final_Data.csv', 'w', newline='') as CsvFile:
            CsvFile.truncate()


if __name__ == "__main__":
    StatsApp().run()
