from time import sleep
from threading import Thread
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
import os
import app.backend.netflix.data_loader as Loading


class NetflixLoadingScreen(MDScreen):

    def _update_label(self, *args):
        if self.__counter < self.__num and self.__loading_screen.finished_loading == 0:
            self.__counter += 1
            percent = self.__counter * 100 // self.__num
            self.manager.get_screen(
                "netflixloadingscreen"
            ).ids.loadinglabel.text = f"{percent}%"
        else:
            self.manager.get_screen(
                "netflixloadingscreen"
            ).ids.loadinglabel.text = f"100%"
            while not self.__loading_screen.finished_loading:
                sleep(1)
            self.__timer.cancel()
            self.skip_processing()

    def _animation_handler(self, *args):
        self.__loading_screen = Loading.NetflixLoadingScreen()
        est_time, self.__num = self.__loading_screen.get_estimated_time(self.__file_path)
        self.backend_thread = Thread(target=self.__loading_screen.start_processing_data)
        self.backend_thread.start()
        self.manager.get_screen(
            "netflixloadingscreen"
        ).ids.estimatedtime.text = f"Estimated time: {round(self.__num * est_time)}s"
        self.__timer = Clock.schedule_interval(self._update_label, est_time)

    def start_processing(self, file_path):
        self.__counter = 0
        self.__file_path = file_path
        self.__timer = Clock
        self.__timer.schedule_once(self._animation_handler, 0)

    def skip_processing(self):
        self.manager.get_screen("netflixuserscreen").generate_screens()
        self.manager.current = "netflixuserscreen"

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *args):
        if key == 27:
            x = MDApp()
            x.stop()
