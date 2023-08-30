import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from models.strategy_model import StrategyModel
from talib import RSI, SMA

class WideScopeStrategy:
    def __init__(self, data_service):
        self.data_service = data_service
        self.df = None

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)

        # Calcular las medias móviles
        df['ma_short'] = SMA(df['close'], timeperiod=20)
        df['ma_long'] = SMA(df['close'], timeperiod=50)

        # Calcular el RSI
        df['rsi'] = RSI(df['close'], timeperiod=14)

        self.df = df
        self.plot_chart("wide_scope_strategy_chart.png")
        print("Estrategia ejecutada correctamente")

    def get_strategy_model(self):
        strategy_name = "Wide Scope Strategy"
        description = "This strategy combines Moving Averages and RSI for a broader market analysis."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)

    def get_data_frame(self):
        return self.df

    def get_signal(self):
        df = self.get_data_frame()

        # Obtener el último precio y RSI
        last_price = df['close'].iloc[-1]
        last_rsi = df['rsi'].iloc[-1]

        # Calcular la tendencia basada en las medias móviles
        trend = self.calculate_trend(df['ma_short'], df['ma_long'])

        # Determinar las señales de compra y venta
        if last_price > df['ma_short'].iloc[-1] and last_price > df['ma_long'].iloc[-1] and last_rsi > 30 and trend == 'uptrend':
            return "buy"
        elif last_price < df['ma_short'].iloc[-1] and last_price < df['ma_long'].iloc[-1] and last_rsi < 70 and trend == 'downtrend':
            return "sell"
        else:
            return "hold"

    def calculate_trend(self, ma_short, ma_long):
        if ma_short.iloc[-1] > ma_long.iloc[-1]:
            return 'uptrend'
        elif ma_short.iloc[-1] < ma_long.iloc[-1]:
            return 'downtrend'
        else:
            return 'sideways'

    def calculate_pivots(self, prices):
        # Encontrar los picos y valles
        peaks, _ = find_peaks(prices, distance=20)
        valleys, _ = find_peaks(-prices, distance=20)
        pivots = pd.Series(0, index=prices.index)

        # Asignar valores a los pivots (1 para resistencia, -1 para soporte)
        for peak in peaks:
            pivots[peak] = 1
        for valley in valleys:
            pivots[valley] = -1

        return pivots

    def plot_chart(self, filename):
        df = self.get_data_frame()

        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.plot(df['timestamp'], df['ma_short'], label='Media Móvil Corta', color='g', linestyle='--')
        plt.plot(df['timestamp'], df['ma_long'], label='Media Móvil Larga', color='r', linestyle='--')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title('Análisis del Mercado con Wide Scope Strategy')
        plt.legend()

        # Guardar el gráfico como una imagen
        plt.savefig(filename)
        plt.close()

# Uso de la estrategia y generación del gráfico
#data_service = YourDataService()  # Reemplaza "YourDataService" con la clase que obtiene los datos desde IQ Option u otro servicio
#strategy = WideScopeStrategy(data_service)
#strategy.execute_strategy()

# Generar el gráfico y guardarlo como una imagen
#strategy.plot_chart("wide_scope_strategy_chart.png")
