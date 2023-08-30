from ports.auth import AuthPort
from iqoptionapi.stable_api import IQ_Option
class AuthAdapter(AuthPort):
    def __init__(self):
        self.api = None
    def get_api(self):
        return self.api
    def login(self, username, password):
        iqoption = IQ_Option(username, password)
        check, reason = iqoption.connect()
        
        if check:
            self.api = iqoption
            return {'status': 'success', 'message': 'Inicio de sesión exitoso'}
        else:
            return {'status': 'error', 'message': 'Credenciales inválidas o fallo al conectar'}
    

