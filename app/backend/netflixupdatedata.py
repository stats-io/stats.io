import numpy as np
import pandas as pd
import app.backend.netflixdataadapter as adapter
import app.backend.tmdbapi as TMBD


class NetflixUpdateData:
    def __init__(self, path):
        data = adapter.NetflixDataAdapter(path)
        data.remake_file()
        self.csv_file = data.csv_file

    def format_user_data(self):
        self.data_array = pd.read_csv(self.csv_file)
        self.data_array = pd.DataFrame(self.data_array)
        self.db_exsist = 0

        with open(
            "app/backend/files/Netflix/UserDB.csv", "r", encoding="utf-8"
        ) as file:
            first_line = file.readline()
            if not first_line:
                pass
            else:
                self.db_exsist = 1

        if self.db_exsist == 0:
            self.data_array = self.look_into_tmbd(self.csv_file, 1)
            if np.isnan(self.data_array.iloc[0, 6]):
                self.data_array.to_csv(
                    "app/backend/files/Netflix/Final_Data.csv", index=False
                )
                self.data_array.to_csv(
                    "app/backend/files/Netflix/LastData.csv", index=False
                )
                self.fetch_into_local_db(self.data_array, 0)
            else:
                self.data_array.to_csv(
                    "app/backend/files/Netflix/LastData.csv", index=False
                )
                self.data_array.to_csv(
                    "app/backend/files/Netflix/Final_Data.csv", index=False
                )
                self.data_array["SumOfTime"] = np.nan
                self.data_array["Dates"] = np.nan
                self.fetch_into_local_db(self.data_array, 0)
        else:
            self.data_array = self.look_into_tmbd(self.csv_file)
            self.data_array = self.look_into_local_db(self.data_array)
            self.dataArray_from_db = self.data_array[self.data_array["actress"].notna()]
            self.data_from_api = self.data_array[~self.data_array["actress"].notna()]
            self.data_from_api = self.get_genres_and_actors(self.data_from_api)
            self.data_array = pd.concat(
                [self.data_from_api, self.dataArray_from_db], ignore_index=True
            )
            self.data_array.to_csv(
                "app/backend/files/Netflix/LastData.csv", index=False
            )
            self.data_array.to_csv(
                "app/backend/files/Netflix/Final_Data.csv", index=False
            )
            self.fetch_into_local_db(self.data_array, 1)
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
        self.data = pd.read_csv("app/backend/files/Netflix/UserDB.csv")
        for ind, row in dataArray.iterrows():
            try:
                filtered_df = self.data.loc[(self.data["title"] == row[0])]
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
        self.user_db = "app/backend/files/Netflix/UserDB.csv"
        if x == 0:
            dataArray.to_csv(self.user_db, index=False)
        else:
            dataArray.to_csv(self.user_db, index=False, mode="a", header=False)
            self.df = pd.read_csv(self.user_db)
            self.df = self.df.drop_duplicates(subset=["title"])
            self.df.to_csv(self.user_db, index=False, mode="w")
