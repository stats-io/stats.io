import os
from os.path import exists

import pandas as pd
from kivy.core.window import Window
from kivy.config import Config
from kivy.logger import Logger
Config.set('kivy', 'exit_on_escape', '0')
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from plyer import filechooser
from androidstorage4kivy import SharedStorage, Chooser

app_folder = os.path.abspath('app/backend/files/Netflix')
user_file_last = os.path.abspath("app/backend/files/Netflix/LastTestFile.csv")
user_data = os.path.abspath('app/backend/files/Netflix/test.csv')
last_data = os.path.abspath('app/backend/files/Netflix/LastData.csv')


class NetflixNewDataScreen(MDScreen):
    __banner_open = False
    dialog = None
    button_press = 0
    private_files = []

    def chooser_callback(self, shared_file_list):
        ss = SharedStorage()
        for shared_file in shared_file_list:
            self.private_files.append(ss.copy_from_shared(shared_file))
        del self.chooser




    def help_banner_handler(self):
        if not self.__banner_open:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.show()
            self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-up"
        else:
            self.parent.get_screen("netflixnewdatascreen").ids.banner.hide()
            self.parent.get_screen("netflixnewdatascreen").ids.bannericon.icon = "chevron-down"
        self.__banner_open = not self.__banner_open

    def start_processing_data(self):
        try:


            # self.parent.get_screen("netflixnewdatascreen").ids.fileadd.text = str(self.private_files[0])
            # df = pd.read_csv(user_data)
            # df.to_csv(user_file_last, index=False)
            self.parent.get_screen("netflixloadingscreen").start_processing(str(self.private_files[0]))
            self.parent.current = "netflixloadingscreen"
        except pd.errors.EmptyDataError:
            self.dialog = MDDialog(
                text="Please, add a file to enjoy your data!",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color="#080808",
                        on_release=self.close_dialog,
                    ),
                ],
            )
            self.dialog.open()

    def close_dialog(self,*args):
        self.dialog.dismiss()

    def skip_processing_data(self):
        try:
            df = pd.read_csv(last_data)
            with open(user_data, "w", newline="") as csv_file:
                csv_file.truncate()
            self.parent.get_screen("netflixloadingscreen").skip_processing()
            self.parent.current = "netflixuserscreen"
        except pd.errors.EmptyDataError:
            self.dialog = MDDialog(
                text="""This is your first time using of this app, 
follow the instructions above and add a csv file!""",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color="#080808",
                        on_release=self.close_dialog,
                    ),
                ],
            )
            self.dialog.open()

    def file_manager_open(self):
        self.chooser = Chooser(self.chooser_callback)
        self.chooser.choose_content('*/*')
        self.parent.current = "netflixnewdatascreen"


    def WrongFile(self):
        self.dialog = MDDialog(
            text="""You add a Wrong file!!!
Follow the instructions above""",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color="#080808",
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.open()

    def __handle_selection(self, selection):
        if selection:
            file_path = os.path.abspath(selection[0])
            file_path = os.path.normpath(file_path)
            file_path = "storage//emulated//0//Downloads//BigCsv.csv"
            self.parent.get_screen("netflixnewdatascreen").ids.filemanagericon.icon = "check-circle"
            self.parent.get_screen("netflixnewdatascreen").ids.fileadd.text = "Chosen file"
            self.parent.get_screen("netflixnewdatascreen").ids.filename.text = f"{selection[0]}"
            self.destination_path = "storage//emulated//0//Downloads//BigCsv.csv"
        else:
            pass

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
                self.parent.current = "mainscreen"


