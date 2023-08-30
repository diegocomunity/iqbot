import csv
import pandas as pd
from abc import ABC, abstractmethod
from ports.data import DataPort

class CSVDataAdapter(DataPort):
    def __init__(self, filename):
        self.filename = filename

    def get_historical_data(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if len(data) == 0:
            raise ValueError("No se encontraron datos históricos en el archivo")

        # Convertir los datos a un DataFrame de Pandas
        df = pd.DataFrame(data[1:], columns=data[0])

        return df

