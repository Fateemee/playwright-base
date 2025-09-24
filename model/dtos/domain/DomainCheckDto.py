from dataclasses import dataclass


@dataclass
class DomainCheckDto:
    available: bool
    domain: str
    premium: bool
    price: int
    reason: str

