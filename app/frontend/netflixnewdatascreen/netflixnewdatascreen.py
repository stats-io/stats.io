from kivymd.uix.screen import MDScreen
from kivy.utils import platform
from plyer import filechooser
# from android.permissions import request_permissions, Permission
import os


class NetflixNewDataScreen(MDScreen):
    _banner_handler = True

    def help_banner_handler(self):
        if self._banner_handler == True:
            self._show_banner()
        else:
            self._hide_banner()
        self._banner_handler = not self._banner_handler

    def start_processing_data(self):
        self.parent.get_screen("netflixloadingscreen").start_animation()
        self.parent.current = "netflixloadingscreen"

    def skip_processing_data(self):
        self.parent.get_screen("netflixloadingscreen").skip_animation()
        self.parent.current = "netflixuserscreen"

    def _show_banner(self):
        self.parent.get_screen("netflixnewdatascreen").ids.banner.show()
        self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-up"

    def _hide_banner(self):
        self.parent.get_screen("netflixnewdatascreen").ids.banner.hide()
        self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-down"

    def on_start(self):
        if platform == "android":
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

    def file_manager_open(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if selection:
            file_path = os.path.abspath(selection[0])
            file_path = os.path.normpath(file_path)
            self.parent.get_screen("netflixnewdatascreen").ids.filemanagericon.icon = "check-circle"
            self.parent.get_screen("netflixnewdatascreen").ids.fileadd.text = "Chosen file"
            self.parent.get_screen("netflixnewdatascreen").ids.filename.text = f"{file_path}"
        else:
            print("No selection")