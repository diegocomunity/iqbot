#autenticación
#from adapters.inbound.auth import AuthAdapter
#from services.auth import AuthService
from adapters.inbound.csv_data_adapter import CSVDataAdapter
from adapters.inbound.iq_option_data_adapter import IQOptionDataAdapter #obtener los datos directamente de iq
from domain.historical_data_service import HistoricalDataService
#strategies - para obtener la tendencia
from domain.trading.strategy.detect_trend import DetectTrend
from domain.trading.strategy.ichimoku_cloud_strategy import IchimokuCloudStrategy
from domain.trading.strategy.ichimoku_clud_support_resistance_strategy import IchimokuCloudSupportResistanceStrategy
#strategies - patrones de velas
from domain.trading.strategy.doji_strategy import DojiStrategy
from domain.trading.strategy.hammer_strategy import HammerStrategy
#soportes y resistencias
from domain.trading.strategy.support_resistance_strategy import SupportResistanceStrategy
#contexto del mercado
from domain.trading.strategy.wide_scope_strategy import WideScopeStrategy
#volumen
from domain.trading.strategy.moving_average_volume_strategy import MovingAverageVolumeStrategy
#order-flow
from domain.trading.strategy.order_flow_strategy import OrderFlowStrategy
#--
from adapters.inbound.trading_input_adapter import TradingInputAdapter #capa de abstracción
from adapters.outbound.trading_output_adapter import TradingOutputAdapter
from infrastructure.trading_repository import TradingOperationRepository
from domain.trading.trading_service import TradingService

#retorna el trading_service con sus adaptadores
def create_trading_service(data_port):
    historical_data_service = HistoricalDataService(data_port)
    #configurando las estrategías de trading
    #patrones de velas
    doji_strategy = DojiStrategy(historical_data_service)
    hammer_strategy = HammerStrategy(historical_data_service)
    #tendencia
    detect_trend_strategy = DetectTrend(historical_data_service)
    ichimoku_cloud_strategy = IchimokuCloudStrategy(historical_data_service)
    ichimoku_cloud_strategy_support_resistance = IchimokuCloudSupportResistanceStrategy(historical_data_service)
    #soportes y resistencia
    support_resistance_strategy = SupportResistanceStrategy(historical_data_service)
    wide_scope_strategy = WideScopeStrategy(historical_data_service)
    #volumen
    order_flow_strategy = OrderFlowStrategy(historical_data_service)
    moving_average_volume_strategy = MovingAverageVolumeStrategy(historical_data_service)
    #configurando adaptadores 
    doji_adapter = TradingInputAdapter(input_port=doji_strategy)
    hammer_adapter = TradingInputAdapter(input_port=hammer_strategy)
    detect_trend_adapter = TradingInputAdapter(input_port=detect_trend_strategy)
    ichimoku_cloud_adapter = TradingInputAdapter(input_port=ichimoku_cloud_strategy)
    ichimoku_cloud_support_resistance_adapter = TradingInputAdapter(input_port=ichimoku_cloud_strategy_support_resistance)
    order_flow_adapter = TradingInputAdapter(input_port=order_flow_strategy)
    support_resistance_adapter = TradingInputAdapter(input_port=support_resistance_strategy)    
    wide_adapter = TradingInputAdapter(input_port=wide_scope_strategy)
    moving_average_volume_adapter = TradingInputAdapter(input_port=moving_average_volume_strategy)
    #configurar los puertos de entrada
    #adaptadores:doji_adapter, hammer_adapter, detect_trend_adapter, ichimoku_cloud_adapter, support_resistance_adapter, moving_average_volume_adapter
    input_ports = [doji_adapter]
    #configurar los puertos de salida
    sqlite = TradingOperationRepository("trading.db")
    output_port=TradingOutputAdapter(sqlite)
    #crear el servicio
    trading_service = TradingService(input_ports, output_port)
    return trading_service

"""
def create_auth_service():
    # Crea una instancia del adaptador de autenticación
    auth_adapter = AuthAdapter()
    # Crea una instancia del servicio de autenticación
    auth_service = AuthService(auth_adapter)
    return auth_service
"""

def execute_trading_operations(params):
    #configurar el puerto para obtener los historicos
    data_port = CSVDataAdapter("adapters/inbound/data/EURUSD_5MN.csv")

    #data_port = IQOptionDataAdapter(api)
    #el servicio para obtener los historicos
    trading_service = create_trading_service(data_port)
    strategy_params = {}
    trading_service.execute_strategies(params)
   

