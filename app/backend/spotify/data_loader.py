import data_updater as PD


class SpotifyLoadingScreen:
    def __init__(self):
        self.finished_loading = 0

    def start_processing_data(self):
        x = PD.SpotifyProcessData()
        x.process_data_from_file()
        self.finished_loading = 1
