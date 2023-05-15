import pandas as pd


class NetflixMainScreen:

     def __init__(self,file="app/backend/files/Final_Data.csv"):
        self.csvFile = self.CSVFile(file)
        self.TotalMoviesWatched = 0
        self.TotalSeriesWatched = 0


    def CSVFile(self,file):
        f = "app/backend/files/"
        test = 1
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            test = 0
        if test == 0:
            files = [f"{f}/LastSmallData.csv", f"{f}/LastBigData.csv"]
            latest_file = max(files, key=os.path.getmtime)
            file = latest_file
            try:
                df = pd.read_csv(file)
            except pd.errors.EmptyDataError:
                if latest_file == f"{f}/LastBigData.csv":
                    file = f"{f}/LastSmallData.csv"
                else:
                    file = f"{f}/LastBigData.csv"
        return file


    def CountMovies(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray["type"] == "film"])

    def CountSeries(self):
        self.DataArray = pd.read_csv(self.csvFile)
        return len(self.DataArray[self.DataArray["type"] == "series"])
