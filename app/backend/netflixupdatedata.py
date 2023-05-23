import numpy as np
import pandas as pd
import app.backend.netflixdataadapter as adapter
import app.backend.tmdbapi as TMBD
import os

last_data = os.path.abspath("app/backend/files/Netflix/LastData.csv")
final_data = os.path.abspath("app/backend/files/Netflix/Final_Data.csv")
UserDB = os.path.abspath("app/backend/files/Netflix/UserDB.csv")

class NetflixUpdateData:
    def __init__(self, path):
        data = adapter.NetflixDataAdapter(path)
        data.remake_file()
        self.csv_file = data.csv_file

    def format_user_data(self):
        data_array = pd.read_csv(self.csv_file)
        data_array = pd.DataFrame(data_array)
        try:
            df = pd.read_csv(UserDB)
            db_exsist = 1
        except pd.errors.EmptyDataError:
            db_exsist = 0

        if db_exsist == 0:
            data_array = self.look_into_tmbd(self.csv_file, 1)
            if np.isnan(data_array.iloc[0, 6]):
                data_array.to_csv(final_data, index=False)
                data_array.to_csv(last_data, index=False )
                self.fetch_into_local_db(data_array, 0)
            else:
                data_array.to_csv(
                    last_data, index=False
                )
                data_array.to_csv(
                    final_data, index=False
                )
                data_array["SumOfTime"] = np.nan
                data_array["Dates"] = np.nan
                self.fetch_into_local_db(data_array, 0)
        else:
            data_array = self.look_into_tmbd(self.csv_file)
            data_array = self.look_into_local_db(data_array)
            dataArray_from_db = data_array[data_array["actress"].notna()]
            data_from_api = data_array[~data_array["actress"].notna()]
            data_from_api = self.get_genres_and_actors(data_from_api)
            data_array = pd.concat(
                [data_from_api,dataArray_from_db], ignore_index=True
            )
            data_array.to_csv(
                last_data, index=False
            )
            data_array.to_csv(
                final_data, index=False
            )
            self.fetch_into_local_db(data_array, 1)
        return 1

    def get_genres_and_actors(self, dataArray):
        api = TMBD.TMBDApi("", 1, dataArray)
        api.get_genres()
        return api.data_array

    def look_into_tmbd(self, csvFile, get_act_and_gen=0):
        api = TMBD.TMBDApi(csvFile, get_act_and_gen)
        api.get_movie_data()
        return api.data_array

    def look_into_local_db(self, dataArray):
        data = pd.read_csv(UserDB)
        for ind, row in dataArray.iterrows():
            try:
                filtered_df = data.loc[(data["title"] == row[0])]
                filtered_df = filtered_df.loc[filtered_df["type"] == row[1]]
                if len(filtered_df) > 0:
                    dataArray.loc[ind, ["genres", "actress"]] = [
                        filtered_df.iloc[0, 3],
                        filtered_df.iloc[0, 5],
                    ]
                else:
                    continue
            except IndexError:
                continue
        return dataArray

    def fetch_into_local_db(self, dataArray, x):
        dataArray["SumOfTime"] = np.nan
        dataArray["Dates"] = np.nan
        dataArray["popularity"] = np.nan
        dataArray["number_of_episodes"] = np.nan
        if x == 0:
            dataArray.to_csv(UserDB, index=False)
        else:
            dataArray.to_csv(UserDB, index=False, mode="a", header=False)
            df = pd.read_csv(UserDB)
            df = df.drop_duplicates(subset=["title"])
            df.to_csv(UserDB, index=False, mode="w")
