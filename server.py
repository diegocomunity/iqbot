from xmlrpc.server import SimpleXMLRPCServer
from adapters.inbound.auth import AuthAdapter
from services.auth import AuthService


# Crea una instancia del adaptador de autenticación
auth_adapter = AuthAdapter()

# Crea una instancia del servicio de autenticación
auth_service = AuthService(auth_adapter)

# Crea una instancia del servidor RPC
server = SimpleXMLRPCServer(('localhost', 8000))
server.register_instance(auth_service)

print("ejecutando servidor rpc en puerto 8000")
# Ejecuta el servidor
server.serve_forever()
