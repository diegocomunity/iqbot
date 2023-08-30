import talib
import pandas as pd
import matplotlib.pyplot as plt
from models.strategy_model import StrategyModel
class MovingAverageVolumeStrategy:
    def __init__(self, data_service, fast_period=10, slow_period=50, volume_window=20):
        self.data_service = data_service
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.volume_window = volume_window

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        # Calcular las medias móviles rápidas y lentas
        df['fast_ma'] = df['close'].rolling(window=self.fast_period).mean()
        df['slow_ma'] = df['close'].rolling(window=self.slow_period).mean()

        # Calcular el volumen promedio
        df['avg_volume'] = df['volume'].rolling(window=self.volume_window).mean()

        # Generar señales de compra y venta
        df['signal'] = 0
        df.loc[(df['fast_ma'] > df['slow_ma']) & (df['volume'] > df['avg_volume']), 'signal'] = 1
        df.loc[(df['fast_ma'] < df['slow_ma']) & (df['volume'] > df['avg_volume']), 'signal'] = -1

        # Generar el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.plot(df.loc[df['signal'] == 1, 'timestamp'], df.loc[df['signal'] == 1, 'close'], '^', markersize=8, color='g', label='Compra')
        plt.plot(df.loc[df['signal'] == -1, 'timestamp'], df.loc[df['signal'] == -1, 'close'], 'v', markersize=8, color='r', label='Venta')
        plt.plot(df['timestamp'], df['fast_ma'], label='Media Móvil Rápida', color='orange')
        plt.plot(df['timestamp'], df['slow_ma'], label='Media Móvil Lenta', color='purple')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title('Estrategia de Cruce de Medias Móviles con Volumen')
        plt.legend()
        plt.grid(True)
        plt.show()

        print("Estrategia ejecutada correctamente")

    def execute_strategy2(self):
        print("\nEjecutando estrategía: moving_arage_volume\n")
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        # Calcular las medias móviles rápidas y lentas
        df['fast_ma'] = df['close'].rolling(window=self.fast_period).mean()
        df['slow_ma'] = df['close'].rolling(window=self.slow_period).mean()

        # Calcular el volumen promedio
        df['avg_volume'] = df['volume'].rolling(window=self.volume_window).mean()

        # Generar señales de compra y venta
        df['signal'] = 0
        df.loc[(df['fast_ma'] > df['slow_ma']) & (df['volume'] > df['avg_volume']), 'signal'] = 1
        df.loc[(df['fast_ma'] < df['slow_ma']) & (df['volume'] > df['avg_volume']), 'signal'] = -1

        # Simulación de operaciones
        trades = df[df['signal'] != 0]
        wins = 0
        losses = 0
        ties = 0

        for i in range(1, len(trades)):
            if trades['signal'].iloc[i] != trades['signal'].iloc[i - 1]:  # Si cambia la señal
                if trades['signal'].iloc[i] == 1:  # Compra
                    if trades['close'].iloc[i] > trades['open'].iloc[i - 1]:  # Ganada
                        wins += 1
                    elif trades['close'].iloc[i] < trades['open'].iloc[i - 1]:  # Perdida
                        losses += 1
                    else:  # Empate
                        ties += 1
                else:  # Venta
                    if trades['close'].iloc[i] < trades['open'].iloc[i - 1]:  # Ganada
                        wins += 1
                    elif trades['close'].iloc[i] > trades['open'].iloc[i - 1]:  # Perdida
                        losses += 1
                    else:  # Empate
                        ties += 1

        print("Simulación de operaciones:")
        print("Ganadas:", wins)
        print("Perdidas:", losses)
        print("Empates:", ties)


    def get_strategy_model(self):
        strategy_name = "Doji Pattern"
        description = "This strategy detects bullish reversal patterns called 'Hammer'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)

    