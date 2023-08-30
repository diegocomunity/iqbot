from domain.trading.trading_strategy_input_port import TradingStrategyInputPort
class TradingService:
    def __init__(self, input_ports:  list[TradingStrategyInputPort], output_port):
        self.input_ports = input_ports
        self.output_port = output_port
    def execute_strategies(self, strategy_params):
        data = None
        for input_port in self.input_ports:
            data = input_port.execute_strategy(strategy_params)
            print("ejecutando: ",data["model"].strategy_name)
            print("precio señal: ", data["signal_date"])
            print("precio", data["signal_price"])
            print("señal: ", data["signal"])
            #print("generando chart")

