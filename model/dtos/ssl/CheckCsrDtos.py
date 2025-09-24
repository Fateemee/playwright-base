from dataclasses import dataclass
from typing import Optional

@dataclass
class CheckCsrDto:
    country: str
    csr:str
    domain: str
    locality: str
    organization: str
    organizationalUnit:str
    state: str
    SAN: Optional[str] = None

