from dataclasses import dataclass

@dataclass
class CheckCsrCommand:
    csr: str
    domain:str
