import talib
import pandas as pd
import matplotlib.pyplot as plt
from models.strategy_model import StrategyModel
class HammerStrategy:
    def __init__(self, data_service):
        self.data_service = data_service
        self.df = None

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)
        df["hammer"]=talib.CDLHAMMER(df['open'].values, df['max'].values, df['min'].values, df['close'].values)
        
 
        # Generar el gráfico
        hammer_df = df[df['hammer'] > 0]

        self.df = hammer_df

        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.plot(hammer_df['timestamp'], hammer_df['close'], 'ro', label='Martillo')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre')
        plt.title('Estrategia de Martillo (Reversión Alcista)')
        plt.legend()
        plt.show()

        print("Estrategia ejecutada correctamente")


    def get_data_frame(self):
        return self.df
    def get_strategy_model(self):
        strategy_name = "Hammer Strategy"
        description = "This strategy detects bullish reversal patterns called 'Hammer'."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.8  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)


