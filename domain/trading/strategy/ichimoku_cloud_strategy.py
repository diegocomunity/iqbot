import talib
import pandas as pd
import matplotlib.pyplot as plt
from models.strategy_model import StrategyModel

class IchimokuCloudStrategy:
    def __init__(self, data_service):
        self.data_service = data_service
        self.ichimoku_df = None

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)

        # Calcular los componentes del Ichimoku Cloud
        tenkan_sen_high = talib.MAX(df['max'], timeperiod=9)
        tenkan_sen_low = talib.MIN(df['min'], timeperiod=9)
        df['tenkan_sen'] = (tenkan_sen_high + tenkan_sen_low) / 2

        kijun_sen_high = talib.MAX(df['max'], timeperiod=26)
        kijun_sen_low = talib.MIN(df['min'], timeperiod=26)
        df['kijun_sen'] = (kijun_sen_high + kijun_sen_low) / 2

        senkou_span_a = (df['tenkan_sen'] + df['kijun_sen']) / 2
        df['senkou_span_a'] = senkou_span_a.shift(26)

        senkou_span_b_high = talib.MAX(df['max'], timeperiod=52)
        senkou_span_b_low = talib.MIN(df['min'], timeperiod=52)
        df['senkou_span_b'] = (senkou_span_b_high + senkou_span_b_low) / 2
        df['senkou_span_b'] = df['senkou_span_b'].shift(26)

        df['chikou_span'] = df['close'].shift(-26)
        self.ichimoku_df = df

        # Generar el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.plot(df['timestamp'], df['tenkan_sen'], label='Tenkan-sen', color='orange')
        plt.plot(df['timestamp'], df['kijun_sen'], label='Kijun-sen', color='purple')
        plt.fill_between(df['timestamp'], df['senkou_span_a'], df['senkou_span_b'], where=df['senkou_span_a'] > df['senkou_span_b'], color='lightgreen', alpha=0.3, label='Ichimoku Cloud')
        plt.fill_between(df['timestamp'], df['senkou_span_a'], df['senkou_span_b'], where=df['senkou_span_a'] < df['senkou_span_b'], color='lightcoral', alpha=0.3)
        plt.plot(df['timestamp'], df['chikou_span'], label='Chikou Span', color='grey', linestyle='dotted')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title('Estrategia Ichimoku Cloud')
        plt.legend()
        plt.show()

        print("Estrategia Ichimoku Cloud ejecutada correctamente")


    def get_strategy_model(self):
        strategy_name = "Ichimoku Cloud"
        description = "This strategy detects bullish reversal patterns called 'Hammer'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.8  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)



    def get_data_frame(self):
        return self.ichimoku_df