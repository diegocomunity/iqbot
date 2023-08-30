import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from models.strategy_model import StrategyModel

class DetectTrend:
    def __init__(self, data_service):
        self.data_service = data_service
        self.df = None

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)

        # Calcular el indicador de Pivots
        df['pivots'] = self.calculate_pivots(df['close'])

        # Encontrar los puntos de soporte y resistencia
        support_levels = df[df['pivots'] == -1]  # Pivots negativos son niveles de soporte
        resistance_levels = df[df['pivots'] == 1]  # Pivots positivos son niveles de resistencia

        # Calcular la tendencia
        trend = self.detect_trend(df['close'])

        self.df = df
        # Calcular el número total de operaciones
        total_trades = len(support_levels) + len(resistance_levels)

        # Calcular el número de operaciones ganadoras y perdedoras
        num_win_trades, num_loss_trades = self.calculate_trades(df, support_levels, resistance_levels)

        # Generar el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.scatter(support_levels['timestamp'], support_levels['close'], color='g', marker='v', label='Soporte')
        plt.scatter(resistance_levels['timestamp'], resistance_levels['close'], color='r', marker='^', label='Resistencia')
        plt.plot(df['timestamp'], df['close'].rolling(window=50).mean(), label='Media Móvil 50 días', color='orange')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title(f'Detección de Soportes, Resistencias y Tendencia ({trend.capitalize()})')
        plt.legend()
        plt.show()

        

        # Mostrar el resultado de las operaciones
        print(f"Tendencia detectada: {trend.capitalize()}")
        print(f"Número total de operaciones: {total_trades}")
        print(f"Número de operaciones ganadoras: {num_win_trades}")
        print(f"Número de operaciones perdedoras: {num_loss_trades}")
        print("Estrategia ejecutada correctamente")

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

    def detect_trend(self, prices):
        # Calcular la media móvil de 50 días
        ma_50 = prices.rolling(window=50).mean()

        # Determinar la tendencia alcista, bajista o de rango
        if prices.iloc[-1] > ma_50.iloc[-1]:
            return "alcista"
        elif prices.iloc[-1] < ma_50.iloc[-1]:
            return "bajista"
        else:
            return "rango"

    def calculate_trades(self, df, support_levels, resistance_levels):
        # Simular las operaciones de compra y venta
        num_win_trades = 0
        num_loss_trades = 0
        for index, row in df.iterrows():
            if index in support_levels.index:
                # Operación de compra en nivel de soporte
                num_win_trades += 1
            elif index in resistance_levels.index:
                # Operación de venta en nivel de resistencia
                num_loss_trades += 1

        return num_win_trades, num_loss_trades

    def get_strategy_model(self):
        strategy_name = "Doji Pattern"
        description = "This strategy detects bullish reversal patterns called 'Hammer'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)

    def get_data_frame(self):
        return self.df