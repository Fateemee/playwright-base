# model/queries/user/user_login_query.py
from dataclasses import dataclass

@dataclass
class UserLoginQuery:
    username: str
    password: str
