import os

from kivymd.uix.screen import MDScreen
from plyer import filechooser


class NetflixNewDataScreen(MDScreen):
    __banner_open = False

    def help_banner_handler(self):
        if not self.__banner_open:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.show()
            self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-up"
        else:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.hide()
            self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-down"
        self.__banner_open = not self.__banner_open

    def start_processing_data(self):
        # [todo] if nothing added don't accept such case
        file_path = self.parent.get_screen("netflixnewdatascreen").ids.filename.text
        self.parent.get_screen("netflixloadingscreen").start_processing(file_path)
        self.parent.current = "netflixloadingscreen"

    def skip_processing_data(self):
        # [todo] cannot skip if there is no file saved before
        self.parent.get_screen("netflixloadingscreen").skip_processing()
        self.parent.current = "netflixuserscreen"

    def file_manager_open(self):
        filechooser.open_file(on_selection=self.__handle_selection)

    def __handle_selection(self, selection):
        if selection:
            file_path = os.path.normpath(os.path.abspath(selection[0]))
            self.parent.get_screen("netflixnewdatascreen").ids.filemanagericon.icon = "check-circle"
            self.parent.get_screen("netflixnewdatascreen").ids.fileadd.text = "Chosen file"
            self.parent.get_screen("netflixnewdatascreen").ids.filename.text = f"{file_path}"
        else:
            pass
