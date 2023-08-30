# Descripción: Este puerto se encarga de recibir los resultados de las estrategias de trading desde el núcleo de la aplicación y enviarlos a la interfaz de usuario, servicios externos u otros destinos de salida.
from abc import ABC, abstractmethod
from models.trading_operation import TradingOperation

class TradingResultOutputPort(ABC):
    @abstractmethod
    def create_table(self):
        pass
    @abstractmethod
    def save_operation(self,TradingOperation):
        pass
    @abstractmethod
    def get_all_operations(self):
        pass
    
