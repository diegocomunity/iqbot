import sys
import os
from xmlrpc.server import SimpleXMLRPCServer
from adapters.inbound.auth import AuthAdapter
from services.auth import AuthService
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
adapters_path = os.path.join(root_path, 'adapters')
sys.path.append(adapters_path)





# Crea una instancia del adaptador de autenticación
#auth_adapter = AuthAdapter()

# Crea una instancia del servicio de autenticación
#auth_service = AuthService(auth_adapter)

# Crea una instancia del servidor RPC
#server = SimpleXMLRPCServer(('localhost', 8000))
#server.register_instance(auth_service)

# Ejecuta el servidor
#server.serve_forever()
