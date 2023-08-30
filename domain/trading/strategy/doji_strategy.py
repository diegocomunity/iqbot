import pandas as pd
import talib
import matplotlib.pyplot as plt
from models.strategy_model import StrategyModel

class DojiStrategy:
    def __init__(self, data_service):
        self.data_service = data_service
        self.df = None

    def execute_strategy(self):
        print("\nEjecutando estrategía: Doji Pattern\n")
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)

        # Calcular los patrones Doji alcistas y bajistas
        df['doji_alcista'] = talib.CDLDOJISTAR(df['open'], df['max'], df['min'], df['close'])
        df['doji_bajista'] = talib.CDLDRAGONFLYDOJI(df['open'], df['max'], df['min'], df['close'])

        # Filtrar las filas que contienen un Doji alcista o bajista
        doji_alcista_df = df[df['doji_alcista'] > 0]
        doji_bajista_df = df[df['doji_bajista'] > 0]

        self.df = df

        # Generar el gráfico con los patrones Doji detectados
        self.plot_chart()

        # Obtener el último precio y fecha de la señal
        last_date = df['timestamp'].iloc[-1]
        last_price = df['close'].iloc[-1]

        # Obtener el modelo de estrategia
        model = self.get_strategy_model()

        # Determinar la señal en función de los patrones detectados
        if not doji_alcista_df.empty:
            signal = "buy"
        elif not doji_bajista_df.empty:
            signal = "sell"
        else:
            signal = "hold"

        # Retornar la señal, el modelo, el DataFrame, la fecha y el precio en un diccionario
        return {
            "signal": signal,
            "model": model,
            "data_frame": df,
            "signal_date": last_date,
            "signal_price": last_price
        }

    def plot_chart(self):
        df = self.df

        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.scatter(df[df['doji_alcista'] > 0]['timestamp'], df[df['doji_alcista'] > 0]['close'], color='g', marker='o', label='Doji alcista')
        plt.scatter(df[df['doji_bajista'] > 0]['timestamp'], df[df['doji_bajista'] > 0]['close'], color='r', marker='o', label='Doji bajista')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title('Análisis del Mercado con Doji Pattern Strategy')
        plt.legend()

        # Mostrar el gráfico
        plt.show()

    def get_strategy_model(self):
        strategy_name = "Doji Pattern"
        description = "This strategy detects bullish and bearish reversal patterns called 'Doji'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)
