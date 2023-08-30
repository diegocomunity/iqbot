import pandas as pd
from iqoptionapi.stable_api import IQ_Option
import time
def connect_iq_option(email, password):
    Iq = IQ_Option(email, password)
    check, reason = Iq.connect()
    if check:
        print("Conexión exitosa a IQ Option")
        return Iq
    else:
        print(f"Error al conectarse a IQ Option: {reason}")
        return None

def get_historical_data(Iq, symbol, interval, count):
    candles = Iq.get_candles(symbol, interval, count, time.time())
    data = []
    for candle in candles:
        data.append({
            'timestamp': convert_timestamp(candle['from']),
            'open': candle['open'],
            'close': candle['close'],
            'min': candle['min'],
            'max': candle['max'],
            'volume': candle['volume'],
        })
    return data

def convert_timestamp(timestamp):
    return pd.to_datetime(timestamp, unit='s')

if __name__ == "__main__":
    email = "correo"
    password = "password"
    symbol = "EURUSD"
    interval = (60*5)  # 1 minute interval
    count = 1000   

    print("conecando a iq: ")
    Iq = connect_iq_option(email, password)
    if Iq:
        print("Descargando script ...")
        data = get_historical_data(Iq, symbol, interval, count)
        data_df = pd.DataFrame(data)

        print(data_df)

        # Guardar en un archivo CSV
        data_df.to_csv('adapters/inbound/data/EURUSD_5MN_test2.csv', index=False)
    print("END SCRIPT")