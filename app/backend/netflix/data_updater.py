import numpy as np
import pandas as pd
import app.backend.netflix.data_adapter as adapter
import app.backend.netflix.tmdb_api as TMBD
import os

last_data = os.path.abspath("app/backend/netflix/database/last_file.csv")
final_data = os.path.abspath("app/backend/netflix/database/final_data.csv")
user_db = os.path.abspath("app/backend/netflix/database/user.csv")


class NetflixUpdateData:
    def __init__(self, path):
        data = adapter.NetflixDataAdapter(path)
        data.remake_file()
        self.csv_file = data.csv_file

    def format_user_data(self):
        data_array = pd.read_csv(self.csv_file)
        data_array = pd.DataFrame(data_array)
        try:
            df = pd.read_csv(user_db)
            db_exsist = 1
        except pd.errors.EmptyDataError:
            db_exsist = 0

        if db_exsist == 0:
            data_array = self.look_into_tmbd(self.csv_file, 1)
            if np.isnan(data_array.iloc[0, 6]):
                data_array.to_csv(final_data, index=False)
                data_array.to_csv(last_data, index=False)
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
                [data_from_api, dataArray_from_db], ignore_index=True
            )
            data_array.to_csv(
                last_data, index=False
            )
            data_array.to_csv(
                final_data, index=False
            )
            self.fetch_into_local_db(data_array, 1)
        return 1

    def get_genres_and_actors(self, data_array):
        api = TMBD.TMBDApi("", 1, data_array)
        api.get_actors_genres()
        return api.data_array

    def look_into_tmbd(self, csv_file, get_act_and_gen=0):
        api = TMBD.TMBDApi(csv_file, get_act_and_gen)
        api.get_movie_data()
        return api.data_array

    def look_into_local_db(self, data_array):
        data = pd.read_csv(user_db)
        for ind, row in data_array.iterrows():
            try:
                filtered_df = data.loc[(data["title"] == row[0])]
                filtered_df = filtered_df.loc[filtered_df["type"] == row[1]]
                if len(filtered_df) > 0:
                    data_array.loc[ind, ["genres", "actress"]] = [
                        filtered_df.iloc[0, 3],
                        filtered_df.iloc[0, 5],
                    ]
                else:
                    continue
            except IndexError:
                continue
        return data_array

    def fetch_into_local_db(self, data_array, x):
        data_array["SumOfTime"] = np.nan
        data_array["Dates"] = np.nan
        data_array["popularity"] = np.nan
        data_array["number_of_episodes"] = np.nan
        if x == 0:
            data_array.to_csv(user_db, index=False)
        else:
            data_array.to_csv(user_db, index=False, mode="a", header=False)
            df = pd.read_csv(user_db)
            df = df.drop_duplicates(subset=["title"])
            df.to_csv(user_db, index=False, mode="w")
