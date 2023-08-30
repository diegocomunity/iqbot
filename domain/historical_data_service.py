from ports.data import DataPort

class HistoricalDataService:
    def __init__(self, data_port: DataPort):
        self.data_port = data_port

    def get_historical_data(self):
        return self.data_port.get_historical_data()
