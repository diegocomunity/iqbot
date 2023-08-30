import time
import pandas as pd
from ports.data import DataPort
class IQOptionDataAdapter(DataPort):
    def __init__(self, api):
        self.api = api
    def convert_timestamp(timestamp):
        return pd.to_datetime(timestamp, unit='s')

    def get_historical_data(self):
        #instrument, timeframe, limit
        instrument = "EURUSD"
        timeframe = 60
        limit = 100

        # Obtener los datos históricos desde IQ Option
        candles = self.api.get_candles(instrument, timeframe, limit, time.time())
        
        # Convertir los datos en un DataFrame de Pandas
        data = {
            'timestamp': [candle['from'] for candle in candles],
            'open': [float(candle['open']) for candle in candles],
            'max': [float(candle['max']) for candle in candles],
            'min': [float(candle['min']) for candle in candles],
            'close': [float(candle['close']) for candle in candles],
            'volume': [float(candle['volume']) for candle in candles]
        }
        df = pd.DataFrame(data)

        return df
