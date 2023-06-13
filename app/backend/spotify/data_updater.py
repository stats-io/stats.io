import pandas as pd
import zipfile
import csv
import os
from spotipy.exceptions import SpotifyException
from requests.exceptions import ConnectionError

new_data = os.path.abspath("app/backend/spotify/database/new_data.csv")
last_data = os.path.abspath("app/backend/spotify/database/last_data.csv")
recently_played_data = os.path.abspath("app/backend/spotify/database/recently_played_tracks.csv")
top_tracks_data = os.path.abspath("app/backend/spotify/database/top_tracks.csv")
top_artists_data = os.path.abspath("app/backend/spotify/database/top_artists.csv")
recommendations_data = os.path.abspath("app/backend/spotify/database/recommendations.csv")


class SpotifyProcessData:
    def __init__(self, file="app/backend/.sample_data/listening_history.zip"):
        self.folder_dir = file

    def process_data_from_spotipy(self, sp):
        try:
            self.get_recently_played_tracks(sp)
            self.get_top_tracks(sp)
            self.get_top_artists(sp)
            self.get_recommendations(sp)
        except ConnectionError:
            pass

    def get_recently_played_tracks(self, sp):
        results = sp.current_user_recently_played(limit=50)

        with open(
                recently_played_data,
                "w",
                newline="",
                encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            headers = ["Nr", "Title", "Artists", "Date"]
            writer.writerow(headers)

            for i, item in enumerate(results["items"]):
                track = item["track"]
                artists = ", ".join([artist["name"] for artist in track["artists"]])
                tmp_date = item["played_at"]
                date = tmp_date[:-5].replace("T", " ")
                row = [i + 1, track["name"], artists, date]
                writer.writerow(row)

    def get_top_tracks(self, sp):
        results = sp.current_user_top_tracks(limit=50)

        with open(
                top_tracks_data,
                "w",
                newline="",
                encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            headers = ["Nr", "Title", "Artists"]
            writer.writerow(headers)

            for i, item in enumerate(results["items"]):
                track = item["name"]
                artist = item["artists"][0]["name"]
                row = [i + 1, track, artist]
                writer.writerow(row)

    def get_top_artists(self, sp):
        results = sp.current_user_top_artists(limit=50)

        with open(
                top_artists_data,
                "w",
                newline="",
                encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            headers = ["Nr", "Artist"]
            writer.writerow(headers)

            for i, item in enumerate(results["items"]):
                artist = item["name"]

                row = [i + 1, artist]
                writer.writerow(row)

    def get_recommendations(self, sp):
        top_artists = pd.read_csv(top_artists_data)
        artists = []

        try:
            for i in range(2):
                search = sp.search(q=top_artists["Artist"][i], type="artist")
                artist_id = search["artists"]["items"][0]["id"]
                artists.append(artist_id)
            results = sp.recommendations(limit=20, seed_genres=artists)
        except SpotifyException:
            results = sp.recommendations(limit=20, seed_genres=["pop"])

        with open(
                recommendations_data,
                "w",
                newline="",
                encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            headers = ["Nr", "Title", "Artist"]
            writer.writerow(headers)

            tracks = results["tracks"]
            index = 1
            for track in tracks:
                artist = track["artists"][0]["name"]
                row = [index, track["name"], artist]
                writer.writerow(row)
                index += 1

    def process_data_from_file(self):
        json_files = []

        with zipfile.ZipFile(self.folder_dir, "r") as zip:
            for file_name in zip.namelist():
                if "StreamingHistory" in file_name and file_name.endswith(".json"):
                    with zip.open(file_name) as file:
                        df = pd.read_json(file)
                        json_files.append(df)

        self.data_array = pd.concat(json_files, ignore_index=True)
        self.data_array.rename(
            columns={
                "endTime": "Date",
                "artistName": "Artist",
                "trackName": "Title",
                "msPlayed": "Time",
            },
            inplace=True,
        )
        self.data_array = self.data_array.iloc[::-1]
        self.data_array = self.data_array.reset_index(drop=True)
        self.data_array.to_csv(new_data)
        self.save_last_data()

    def save_last_data(self):
        self.data_array.to_csv(last_data)
