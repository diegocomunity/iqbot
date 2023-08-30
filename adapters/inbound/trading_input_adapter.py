from domain.trading.trading_strategy_input_port import TradingStrategyInputPort

class TradingInputAdapter:
    def __init__(self, input_port: TradingStrategyInputPort):
        self.trading_strategy = input_port

    def execute_strategy(self, strategy_params):
        print("ejecutando adaptador")

        data = self.trading_strategy.execute_strategy()
        return data
        #print(self.trading_strategy.get_signal())
#        price = strategy_params["price"]
#        self.trading_strategy.update_price(price)
#
#        signal = self.trading_strategy.generate_signal()
#        if signal == "BUY":
            # Lógica para enviar la señal de compra al sistema o realizar otras acciones
#            print("Señal de compra generada")

        # Puedes devolver la señal generada o realizar otras acciones según sea necesario
        #return signal
    def plot_chart():
        self.trading_strategy.plot_chart()
