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
        print("\nEjecutando estrategía: moving_average_volume\n")
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
        df.loc[df['signal'] == 0, 'signal'] = 0

        # Simulación de operaciones
        simulated_trades = self.simulate_trades(df)

        # Generar el DataFrame con la información de las operaciones
        operations_df = pd.DataFrame(simulated_trades)
        # Guardar el DataFrame en un archivo CSV
        operations_df.to_csv('adapters/outbound/moving_avarage_volume_1.csv', index=False)

        # Obtener el último volumen y volumen promedio
        last_volume = df['volume'].iloc[-1]
        last_volume_avg = df['avg_volume'].iloc[-1]

        # Obtener la fecha y precio en el que se generó la señal
        last_date = df['timestamp'].iloc[-1]
        last_price = df['close'].iloc[-1]

        # Obtener el modelo de estrategia
        model = self.get_strategy_model()

        # Retornar la señal, el modelo, el DataFrame, la fecha y el precio en un diccionario
        return {
            "signal": df['signal'].iloc[-1],
            "model": model,
            "data_frame": df,
            "signal_date": last_date,
            "signal_price": last_price
        }

    def simulate_trades(self, df):
        trades = df[df['signal'] != 0]
        simulated_trades = []
        for i in range(1, len(trades)):
            if trades['signal'].iloc[i] != trades['signal'].iloc[i - 1]:  # Si cambia la señal
                if trades['signal'].iloc[i] == 1:  # Compra
                    if trades['close'].iloc[i] > trades['open'].iloc[i - 1]:  # Ganada
                        result = 'Win'
                    elif trades['close'].iloc[i] < trades['open'].iloc[i - 1]:  # Perdida
                        result = 'Loss'
                    else:  # Empate
                        result = 'Tie'
                else:  # Venta
                    if trades['close'].iloc[i] < trades['open'].iloc[i - 1]:  # Ganada
                        result = 'Win'
                    elif trades['close'].iloc[i] > trades['open'].iloc[i - 1]:  # Perdida
                        result = 'Loss'
                    else:  # Empate
                        result = 'Tie'

                simulated_trades.append({
                    'Signal Date': trades['timestamp'].iloc[i],
                    'Signal Price': trades['close'].iloc[i - 1],
                    'Exit Price': trades['close'].iloc[i],
                    'Action': 'Buy' if trades['signal'].iloc[i] == 1 else 'Sell',
                    'Result': result
                })

        return simulated_trades

    def get_strategy_model(self):
        strategy_name = "Moving Average Volume Strategy"
        description = "This strategy is based on moving average crossover combined with volume analysis."
        parameters = {
            "Fast Period": self.fast_period,
            "Slow Period": self.slow_period,
            "Volume Window": self.volume_window
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)
