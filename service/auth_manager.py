# services/auth_manager.py
class AuthManager:
    _token: str = None

    @classmethod
    def set_token(cls, token: str):
        cls._token = token

    @classmethod
    def get_token(cls):
        return cls._token
