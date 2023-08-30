import talib
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from models.strategy_model import StrategyModel

class IchimokuCloudSupportResistanceStrategy:
    def __init__(self, data_service):
        self.data_service = data_service

    def calculate_ichimoku_cloud(self, df):
        high_prices = df['max'].astype(float)
        low_prices = df['min'].astype(float)
        close_prices = df['close'].astype(float)

        # Calcular los componentes del Ichimoku Cloud
        tenkan_sen_high = talib.MAX(high_prices, timeperiod=9)
        tenkan_sen_low = talib.MIN(low_prices, timeperiod=9)
        df['tenkan_sen'] = (tenkan_sen_high + tenkan_sen_low) / 2

        kijun_sen_high = talib.MAX(high_prices, timeperiod=26)
        kijun_sen_low = talib.MIN(low_prices, timeperiod=26)
        df['kijun_sen'] = (kijun_sen_high + kijun_sen_low) / 2

        senkou_span_a = (df['tenkan_sen'] + df['kijun_sen']) / 2
        df['senkou_span_a'] = senkou_span_a.shift(26)

        senkou_span_b_high = talib.MAX(high_prices, timeperiod=52)
        senkou_span_b_low = talib.MIN(low_prices, timeperiod=52)
        df['senkou_span_b'] = (senkou_span_b_high + senkou_span_b_low) / 2
        df['senkou_span_b'] = df['senkou_span_b'].shift(26)

        df['chikou_span'] = close_prices.shift(-26)

    def calculate_support_resistance(self, prices):
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

    def generate_signals(self, df):
        signals = []

        for i in range(len(df)):
            if df['tenkan_sen'][i] > df['kijun_sen'][i] and df['close'][i] > df['senkou_span_a'][i] and df['close'][i] > df['senkou_span_b'][i] and df['chikou_span'][i] > df['close'][i]:
                signals.append("BUY")
            elif df['tenkan_sen'][i] < df['kijun_sen'][i] and df['close'][i] < df['senkou_span_a'][i] and df['close'][i] < df['senkou_span_b'][i] and df['chikou_span'][i] < df['close'][i]:
                signals.append("SELL")
            else:
                signals.append("HOLD")

        return signals
    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)

        # Calcular el Ichimoku Cloud
        self.calculate_ichimoku_cloud(df)

        # Calcular los niveles de soporte y resistencia
        prices = df['close']
        pivots = self.calculate_support_resistance(prices)
        df['pivots'] = pivots

        # Generar señales de compra o venta basadas en Ichimoku Cloud y soportes/resistencias
        signals = self.generate_signals(df)

        # Simulación de operaciones basada en las señales generadas
        total_trades = 0
        winning_trades = 0
        losing_trades = 0
        position = None

        for i in range(len(df)):
            if signals[i] == "BUY" and position is None:
                position = "BUY"
                total_trades += 1
            elif signals[i] == "SELL" and position == "BUY":
                position = None
                winning_trades += 1
                total_trades += 1
            elif signals[i] == "SELL" and position is None:
                position = "SELL"
                total_trades += 1
            elif signals[i] == "BUY" and position == "SELL":
                position = None
                winning_trades += 1
                total_trades += 1

        losing_trades = total_trades - winning_trades

        # Mostrar el resumen
        print("\nResumen:")
        print(f"Total de operaciones: {total_trades}")
        print(f"Operaciones ganadas: {winning_trades}")
        print(f"Operaciones perdidas: {losing_trades}")



    def get_strategy_model(self):
        strategy_name = "Ichimoku Cloud Supports and resistance"
        description = "This strategy detects bullish reversal patterns called 'Hammer'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.8  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)




