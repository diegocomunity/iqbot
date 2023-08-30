#Descripción: Este puerto se encarga de recibir las señales de trading y enviarlas al núcleo de la aplicación para su procesamiento.
from abc import ABC, abstractmethod

class TradingStrategyInputPort(ABC):
    @abstractmethod
    def execute_strategy(self, strategy_params):
        pass

    @abstractmethod
    def update_price(self, price):
        pass

    @abstractmethod
    def get_signal(self):
        pass
    
    @abstractmethod
    def get_strategy_model(self):
        pass
    @abstractmethod
    def get_data_frame(self):
        pass