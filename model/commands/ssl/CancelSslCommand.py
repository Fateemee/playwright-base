from dataclasses import dataclass

@dataclass
class CancelSslCommand:
    type: str
    domain:str
    provider:str
