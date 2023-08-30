from abc import ABC, abstractmethod

class AuthPort(ABC):
    @abstractmethod
    def login(self, username, password):
        pass
    @abstractmethod
    def get_api(self):
        pass
