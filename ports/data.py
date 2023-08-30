import csv
from abc import ABC, abstractmethod

class DataPort(ABC):
    @abstractmethod
    def get_historical_data(self):
        pass