import pandas as pd
import zipfile


class SpotifyProcessData:

    def __init__(self,file="app/backend/files/Spotify/my_spotify_data.zip"):
        self.FolderDir = file

    def ProcessDataFromFile(self):
        json_files = []

        with zipfile.ZipFile(self.FolderDir, "r") as zip:
            for file_name in zip.namelist():
                if "StreamingHistory" in file_name and file_name.endswith(".json"):
                    with zip.open(file_name) as file:
                        df = pd.read_json(file)
                        json_files.append(df)

        self.DataArray = pd.concat(json_files, ignore_index=True)
        self.DataArray.rename(
            columns={
                "endTime": "Date",
                "artistName": "Artist",
                "trackName": "Title",
                "msPlayed": "Time",
            },
            inplace=True,
        )
        self.DataArray = self.DataArray.iloc[::-1]
        self.DataArray = self.DataArray.reset_index(drop=True)
        self.DataArray.to_csv("app/backend/files/Spotify/Spotify_Data.csv")
        self.SaveLastData()

    def SaveLastData(self):
        self.DataArray.to_csv("app/backend/files/Spotify/Last_Data.csv")
