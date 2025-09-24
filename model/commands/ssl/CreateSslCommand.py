from dataclasses import dataclass, asdict
from typing import Optional, Dict

@dataclass
class Requester:
    firstName: str
    lastName: str
    email: str
    phone: str

@dataclass
class CreateSslCommand:
    provider: str
    csr: str
    requester: Requester
    product: int
    username: Optional[str]
    method: str
    san: Optional[str]
    domain: str

    def to_dict(self) -> Dict:
        # اینجا requester رو تبدیل به dict می‌کنیم با فرمت مورد نظر API
        body = asdict(self)
        requester_dict = body.pop("requester")
        # تبدیل به ساختار مورد انتظار API: requester[firstName]: "Ali", ...
        for key, value in requester_dict.items():
            body[f"requester[{key}]"] = value
        return body
