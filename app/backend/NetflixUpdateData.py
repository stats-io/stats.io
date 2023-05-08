import json
import datetime
import pandas as pd
import numpy as np
import requests

class NetflixUpdateData():

    def __init__(self, path):
        data = NetflixDataAdapter(path)
        data.remakeFile()
        self.csvFile = data.csvFile
        self.dbpath = 'UserDB.csv'

    def formatUserData(self):
        self.dataArray = pd.read_csv(self.csvFile)
        self.dataArray = pd.DataFrame(self.dataArray)
        self.DBexsist = 0

        with open(self.dbpath, 'r', encoding='utf-8') as file:
            first_line = file.readline()
            if not first_line:
                pass
            else:
                self.DBexsist = 1

        if self.DBexsist == 0:
            self.dataArray = self.lookintoTMBD(self.csvFile,1)
            if np.isnan(self.dataArray.iloc[0,6]):
                self.dataArray.to_csv('Final_Data.csv', index=False)
                self.dataArray.to_csv('LastSmallData.csv',index=False)
                self.fetchintoLocalDb(self.dataArray,0)
            else:
                self.dataArray.to_csv('LastBigData.csv', index=False)
                self.dataArray.to_csv('Final_Data.csv', index=False)
                self.dataArray['SumOfTime'] = np.nan
                self.dataArray['Dates'] = np.nan
                self.fetchintoLocalDb(self.dataArray,0)
        else:
            self.dataArray = self.lookintoTMBD(self.csvFile)
            self.dataArray = self.lookintoLocalDb(self.dataArray)
            self.dataArray_from_db = self.dataArray[self.dataArray['actress'].notna()]
            self.data_from_api = self.dataArray[~self.dataArray['actress'].notna()]
            self.data_from_api = self.get_Genres_and_Actors(self.data_from_api)
            self.dataArray = pd.concat([self.data_from_api, self.dataArray_from_db],ignore_index=True)
            if np.isnan(self.dataArray.iloc[0,6]):
                self.dataArray.to_csv('LastSmallData.csv')
            else:
                self.dataArray.to_csv('LastBigData.csv')
            self.dataArray.to_csv('Final_Data.csv', index=False)
            self.fetchintoLocalDb(self.dataArray,1)

    def get_Genres_and_Actors(self,dataArray):
        api = TMBDApi('',1,dataArray)
        api.getGenres()
        return api.dataArray


    def lookintoTMBD(self,csvFile,get_act_and_gen = 0):
        api = TMBDApi(csvFile,get_act_and_gen)
        api.getMovieData()
        return api.dataArray

    def lookintoLocalDb(self,dataArray):
        self.data = pd.read_csv('UserDB.csv')
        for ind, row in dataArray.iterrows():
            try:
                filtered_df = self.data.loc[(self.data['title'] == row[0])]
                filtered_df = filtered_df.loc[filtered_df['type'] == row[1]]
                if len(filtered_df) > 0:
                    dataArray.loc[ind, ['genres', 'actress']] = [filtered_df.iloc[0, 3],filtered_df.iloc[0, 5]]
                else:
                    continue
            except IndexError:
                continue
        return dataArray

    def fetchintoLocalDb(self,dataArray,x):
        dataArray['SumOfTime'] = np.nan
        dataArray['Dates'] = np.nan
        dataArray['popularity'] = np.nan
        dataArray['number_of_episodes'] = np.nan
        if x == 0:
            dataArray.to_csv('UserDB.csv', index=False)
        else:
            dataArray.to_csv('UserDB.csv', index = False, mode = 'a',header = False)
            self.df = pd.read_csv('UserDB.csv')
            self.df = self.df.drop_duplicates(subset=['title'])
            self.df.to_csv('UserDB.csv', index = False, mode = 'w')
