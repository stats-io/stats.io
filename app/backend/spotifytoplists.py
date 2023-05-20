import pandas as pd


class SpotifyTopList:
    def __init__(self):
        self.csv_file = self.read_csv()

    def read_csv(self):
        self.last = "app/backend/files/Spotify/Last_Data.csv"
        self.new = "app/backend/files/Spotify/Spotify_Data.csv"
        try:
            self.data_array = pd.read_csv(self.new)
            return self.new
        except pd.errors.EmptyDataError:
            pass
        try:
            self.data_array = pd.read_csv(self.last)
            return self.last
        except pd.errors.EmptyDataError:
            return None

    def ms_converter(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60

        seconds %= 60
        minutes %= 60

        if minutes < 10:
            minutes = f"0{minutes}"
        if hours < 10:
            hours = f"0{hours}"
        if seconds < 10:
            seconds = f"0{seconds}"

        return f"{hours}:{minutes}:{seconds}"

    def artist_top_list(self):
        self.month_artist_list = self.dates(1)
        self.half_year_artist_list = self.dates(2)
        self.all_time_artist_list = self.dates(3)
        month_list = self.artist_dictionary(self.month_artist_list)
        half_year_list = self.artist_dictionary(self.half_year_artist_list)
        all_time_list = self.artist_dictionary(self.all_time_artist_list)
        return (
            self.data_converter(month_list),
            self.data_converter(half_year_list),
            self.data_converter(all_time_list),
        )

    def dates(self, time):
        tmp_df = self.data_array
        tmp_df["Date"] = pd.to_datetime(tmp_df["Date"])
        tmp_df = tmp_df.drop("Unnamed: 0", axis=1)
        newest_data = tmp_df["Date"].max()
        if time == 1:
            data = tmp_df[tmp_df["Date"] >= newest_data - pd.DateOffset(months=1)]
        elif time == 2:
            data = tmp_df[tmp_df["Date"] >= newest_data - pd.DateOffset(months=6)]
        else:
            data = tmp_df
        return data

    def artist_dictionary(self, data_array):
        artist_dic = {}
        for ind, row in data_array.iterrows():
            artist = row["Artist"]
            time = row["Time"]
            if artist in artist_dic.keys():
                artist_dic[artist] += time
            else:
                artist_dic[artist] = time
        artist_df = pd.DataFrame.from_dict(
            artist_dic, orient="index", columns=["value"]
        )
        artist_df = artist_df.sort_values("value", ascending=False).head(10)
        return artist_df

    def data_converter(self, data_array):
        for ind, row in data_array.iterrows():
            data_array.loc[ind, "value"] = self.ms_converter(row["value"])
        return data_array

    def song_top_list(self):
        self.month_song_list = self.dates(1)
        self.half_year_song_list = self.dates(2)
        self.alltime_song_list = self.dates(3)
        month_list = self.song_dictionary(self.month_song_list)
        half_year_list = self.song_dictionary(self.half_year_song_list)
        all_time_list = self.song_dictionary(self.alltime_song_list)
        return (
            self.data_converter(month_list),
            self.data_converter(half_year_list),
            self.data_converter(all_time_list),
        )

    def song_dictionary(self, data_array):
        song_dic = {}
        for ind, row in data_array.iterrows():
            song = row["Title"]
            time = row["Time"]
            if song in song_dic.keys():
                song_dic[song] += time
            else:
                song_dic[song] = time
        song_df = pd.DataFrame.from_dict(song_dic, orient="index", columns=["value"])
        song_df = song_df.sort_values("value", ascending=False).head(10)
        return song_df

    def most_listened_day(self):
        data_array = pd.read_csv(self.csv_file)
        data_array = data_array.drop("Unnamed: 0", axis=1)
        data_array["Date"] = data_array["Date"].apply(lambda x: x.split(" ")[0])
        data_array = data_array.groupby("Date").agg({"Time": "sum"}).reset_index()
        data_array = data_array.sort_values("Time", ascending=False).head(10)
        for ind, row in data_array.iterrows():
            data_array.loc[ind, "Time"] = self.ms_converter(row["Time"])
        data_array.reset_index(drop=True, inplace=True)
        return data_array
