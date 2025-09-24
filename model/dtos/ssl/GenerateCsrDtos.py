from typing import Optional
from dataclasses import dataclass

@dataclass
class GenerateCsrDto:
    country: str
    csr: str
    domain: str
    locality: str
    organization: str
    private_key: str
    state: str
    SAN: Optional[str] = None 
