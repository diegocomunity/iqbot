from ports.auth import AuthPort

class AuthService:
    def __init__(self, auth_port: AuthPort):
        self.auth_port = auth_port
    
    def login(self, username, password):
        return self.auth_port.login(username, password)
    def get_api(self):
        return self.auth_port.get_api()
