import os
import pandas as pd
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from plyer import filechooser

app_folder = os.path.abspath('app/backend/files/Netflix')
user_file_last = os.path.abspath("app/backend/files/Netflix/LastTestFile.csv")
user_data = os.path.abspath('app/backend/files/Netflix/test.csv')
last_data = os.path.abspath('app/backend/files/Netflix/LastData.csv')

class NetflixNewDataScreen(MDScreen):
    __banner_open = False
    dialog = None

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
            df = pd.read_csv(user_data)
            df.to_csv(user_file_last, index=False)
            self.parent.get_screen("netflixloadingscreen").start_processing(self.destination_path)
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
        filechooser.open_file(on_selection=self.__handle_selection)


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
            file_path = selection[0]
            try:
                df = pd.read_csv(file_path)
                required_columns_1 = ["Title", "Date"]
                required_columns_2 = ["Profile Name", "Start Time", "Duration", "Attributes", "Title",
                                      "Supplemental Video Type", "Device Type", "Bookmark", "Latest Bookmark",
                                      "Country"]
                if all(column in df.columns for column in required_columns_1) or all(column in df.columns for column in required_columns_2):
                    self.parent.get_screen("netflixnewdatascreen").ids.filemanagericon.icon = "check-circle"
                    self.parent.get_screen("netflixnewdatascreen").ids.fileadd.text = "Chosen file"
                    self.parent.get_screen("netflixnewdatascreen").ids.filename.text = f"{selection[0]}"
                    self.destination_path = os.path.join(app_folder, 'test.csv')
                    df.to_csv(self.destination_path, index=False)
                else:
                    self.WrongFile()
            except Exception:
                self.WrongFile()

        else:
            pass
