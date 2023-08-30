import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from models.strategy_model import StrategyModel


class OrderFlowStrategy:
    def __init__(self, data_service):
        self.data_service = data_service
        self.df = None

    def execute_strategy(self):
        df = self.data_service.get_historical_data()
        df['open'] = df['open'].astype(float)
        df['max'] = df['max'].astype(float)
        df['min'] = df['min'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        # Calcular el volumen promedio
        df['volume_avg'] = df['volume'].rolling(window=20).mean()

        # Obtener el último volumen y volumen promedio
        last_volume = df['volume'].iloc[-1]
        last_volume_avg = df['volume_avg'].iloc[-1]

        # Determinar las señales de compra y venta
        if last_volume > last_volume_avg:
            signal = "buy"
        elif last_volume < last_volume_avg:
            signal = "sell"
        else:
            signal = "hold"

        # Agregar la columna 'signal' al DataFrame
        df['signal'] = signal

        self.df = df



        # Simular las operaciones
        self.simulate_trades()

        # Obtener el modelo de estrategia
        model = self.get_strategy_model()

        print("Estrategia ejecutada correctamente")

        # Retornar la señal, el modelo, el DataFrame, la fecha y el precio en un diccionario
        return {
            "signal": signal,
            "model": model,
            "data_frame": df,
            "signal_date": df['timestamp'].iloc[-1],
            "signal_price": df['close'].iloc[-1]
        }


    def simulate_trades(self):
        df = self.df
        capital = 1000000.0  # Capital inicial en dólares
        position_size = 10000.0  # Tamaño de posición en dólares
        win_amount = 1.5  # Cantidad ganada por operación exitosa (2.0 significa el doble de la inversión) 

        # Variables para el seguimiento de la simulación
        num_trades = 0
        num_wins = 0
        num_losses = 0
        results = []  # Lista para almacenar los resultados de cada operación

        for i in range(len(df) - 1):  # Recorremos hasta el penúltimo elemento para evitar un índice fuera de rango
            signal = df.loc[i, 'signal']
            entry_price = df.loc[i, 'close']
            exit_price = df.loc[i + 1, 'close']

            if signal == "buy":
                # Simular operación de compra
                capital -= position_size
                if exit_price > entry_price:
                    # Operación ganadora
                    capital += position_size * win_amount
                    num_wins += 1
                    result = "win"
                else:
                    # Operación perdedora
                    num_losses += 1
                    result = "loss"

                num_trades += 1
            elif signal == "sell":
                # Simular operación de venta
                capital += position_size
                if exit_price < entry_price:
                    # Operación ganadora
                    capital += position_size * win_amount
                    num_wins += 1
                    result = "win"
                else:
                    # Operación perdedora
                    num_losses += 1
                    result = "loss"

                num_trades += 1

            # Agregar el resultado de la operación a la lista
            results.append([df.loc[i, 'timestamp'], entry_price, exit_price, signal, result])

        # Crear DataFrame con los resultados
        results_df = pd.DataFrame(results, columns=['Fecha', 'Precio Entrada', 'Precio Cierre', 'Tipo Entrada', 'Resultado'])

        # Guardar DataFrame en archivo CSV
        results_df.to_csv('order_flow_strategy_results.csv', index=False)

        print(f"Capital final: {capital:.2f} dólares")
        print(f"Número total de operaciones: {num_trades}")
        print(f"Número de operaciones ganadoras: {num_wins}")
        print(f"Número de operaciones perdedoras: {num_losses}")


    def get_strategy_model(self):
        strategy_name = "Order Flow Strategy"
        description = "This strategy is based on order flow analysis using volume data."
        parameters = {
            # Aquí puedes agregar los parámetros de la estrategia, si los hay
        }
        signal_strength = 0.2  # Aquí puedes calcular o definir la fuerza de la señal

        return StrategyModel(strategy_name, description, parameters, signal_strength)

    def plot_chart(self):
        df = self.df
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['close'], label='Precio de cierre', color='b')
        plt.bar(df['timestamp'], df['volume'], label='Volumen', color='c', alpha=0.3)
        plt.plot(df['timestamp'], df['volume_avg'], label='Volumen Promedio', color='g', linestyle='--')
        plt.xlabel('Fecha')
        plt.ylabel('Valor de cierre / Volumen')
        plt.title('Análisis del Mercado con Order Flow Strategy')
        plt.legend()

        # Guardar el gráfico como una imagen
        plt.savefig("order_flow_strategy_chart.png")
        plt.close()


        df = self.df
        capital = 10000  # Capital inicial en dólares
        position_size = 1000  # Tamaño de posición en dólares
        win_amount = 100  # Cantidad ganada por operación exitosa en dólares

        # Variables para el seguimiento de la simulación
        num_trades = 0
        num_wins = 0
        num_losses = 0

        # Listas para almacenar los resultados de las operaciones
        entry_dates = []
        entry_prices = []
        exit_prices = []
        trade_results = []

        for index, row in df.iterrows():
            # Obtener la señal de la estrategia directamente del DataFrame
            signal = row['signal']

            if signal == "buy":
                # Simular operación de compra
                entry_price = row['close']
                entry_dates.append(row['timestamp'])
                entry_prices.append(entry_price)

                capital -= position_size
                if row['close'] > df['close'].shift(-1).loc[index]:
                    # Operación ganadora
                    capital += win_amount
                    num_wins += 1
                    exit_prices.append(df['close'].shift(-1).loc[index])
                    trade_results.append("win")
                else:
                    # Operación perdedora
                    num_losses += 1
                    exit_prices.append(df['close'].shift(-1).loc[index])
                    trade_results.append("loss")

                num_trades += 1
            elif signal == "sell":
                # Simular operación de venta
                entry_price = row['close']
                entry_dates.append(row['timestamp'])
                entry_prices.append(entry_price)

                capital += position_size
                if row['close'] < df['close'].shift(-1).loc[index]:
                    # Operación ganadora
                    capital += win_amount
                    num_wins += 1
                    exit_prices.append(df['close'].shift(-1).loc[index])
                    trade_results.append("win")
                else:
                    # Operación perdedora
                    num_losses += 1
                    exit_prices.append(df['close'].shift(-1).loc[index])
                    trade_results.append("loss")

                num_trades += 1

        print(f"Capital final: {capital:.2f} dólares")
        print(f"Número total de operaciones: {num_trades}")
        print(f"Número de operaciones ganadoras: {num_wins}")
        print(f"Número de operaciones perdedoras: {num_losses}")

        # Crear un DataFrame con los resultados de las operaciones
        trade_data = {
            'Entry Date': entry_dates,
            'Entry Price': entry_prices,
            'Exit Price': exit_prices,
            'Result': trade_results
        }
        trade_df = pd.DataFrame(trade_data)

        # Guardar los resultados en un archivo CSV
        trade_df.to_csv('order_flow_strategy_trades.csv', index=False)