from typing import Optional
from dataclasses import dataclass

@dataclass
class UserLoginDto:
    access_token: str
    expires_in: int
    refresh_expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    session_state: Optional[str] = None
    token_type: Optional[str] = None