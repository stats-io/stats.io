import pandas as pd


class SpotifyTopList:

    def __init__(self):
        self.csvFile = self.ReadCSV()

    def ReadCSV(self):
        self.Last = "app/backend/files/Spotify/Last_Data.csv"
        self.new = "app/backend/files/Spotify/Spotify_Data.csv"
        try:
            self.DataArray = pd.read_csv(self.new)
            return self.new
        except pd.errors.EmptyDataError:
            pass
        try:
            self.DataArray = pd.read_csv(self.Last)
            return self.Last
        except pd.errors.EmptyDataError:
            return None

    def msConverter(self, ms):
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

    def ArtistTopList(self):
        self.MonthArtistList = self.Dates(1)
        self.halfYearArtistList = self.Dates(2)
        self.AllTimeArtistList = self.Dates(3)
        month_list = self.ArtistDictionary(self.MonthArtistList)
        half_year_list = self.ArtistDictionary(self.halfYearArtistList)
        all_time_list = self.ArtistDictionary(self.AllTimeArtistList)
        return self.DataConverter(month_list), self.DataConverter(half_year_list), self.DataConverter(all_time_list)

    def Dates(self, time):
        tmp_df = self.DataArray
        tmp_df['Date'] = pd.to_datetime(tmp_df['Date'])
        tmp_df = tmp_df.drop('Unnamed: 0', axis=1)
        newest_data = tmp_df['Date'].max()
        if time == 1:
            Data = tmp_df[tmp_df['Date'] >= newest_data - pd.DateOffset(months=1)]
        elif time == 2:
            Data = tmp_df[tmp_df['Date'] >= newest_data - pd.DateOffset(months=6)]
        else:
            Data = tmp_df
        return Data

    def ArtistDictionary(self, DataArray):
        Artist_dic = {}
        for ind, row in DataArray.iterrows():
            Artist = row['Artist']
            time = row['Time']
            if Artist in Artist_dic.keys():
                Artist_dic[Artist] += time
            else:
                Artist_dic[Artist] = time
        Artist_df = pd.DataFrame.from_dict(Artist_dic, orient="index", columns=["value"])
        Artist_df = Artist_df.sort_values("value", ascending=False).head(10)
        return Artist_df

    def DataConverter(self, DataArray):
        for ind, row in DataArray.iterrows():
            DataArray.loc[ind, 'value'] = self.msConverter(row['value'])
        return DataArray

    def SongTopList(self):
        self.MonthSongList = self.Dates(1)
        self.HalfYearSongList = self.Dates(2)
        self.AlltimeSongList = self.Dates(3)
        month_list = self.SongDictionary(self.MonthSongList)
        half_year_list = self.SongDictionary(self.HalfYearSongList)
        all_time_list = self.SongDictionary(self.AlltimeSongList)
        return self.DataConverter(month_list), self.DataConverter(half_year_list), self.DataConverter(all_time_list)

    def SongDictionary(self, DataArray):
        Song_dic = {}
        for ind, row in DataArray.iterrows():
            Song = row['Title']
            time = row['Time']
            if Song in Song_dic.keys():
                Song_dic[Song] += time
            else:
                Song_dic[Song] = time
        Song_df = pd.DataFrame.from_dict(Song_dic, orient="index", columns=["value"])
        Song_df = Song_df.sort_values("value", ascending=False).head(10)
        return Song_df

    def MostListenedDay(self):
        DataArray = pd.read_csv(self.csvFile)
        DataArray = DataArray.drop('Unnamed: 0', axis=1)
        DataArray['Date'] = DataArray['Date'].apply(lambda x: x.split(' ')[0])
        DataArray = DataArray.groupby('Date').agg({'Time': 'sum'}).reset_index()
        DataArray = DataArray.sort_values('Time', ascending=False).head(10)
        for ind, row in DataArray.iterrows():
            DataArray.loc[ind, 'Time'] = self.msConverter(row['Time'])
        DataArray.reset_index(drop=True, inplace=True)
        return DataArray
