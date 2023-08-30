from domain.trading.trading_result_output_port import TradingResultOutputPort
from models.trading_operation import TradingOperation

class TradingOutputAdapter:
    def __init__(self, output_port: TradingResultOutputPort):
        self.trading_repository = output_port
    def save_operation(self, operation:TradingOperation):
        self.trading_repository.save_operation(operation)
    def create_table(self):
        self.trading_repository.create_table()