from dataclasses import dataclass

@dataclass
class GenerateCsrCommand:
    country: str
    state: str
    locality:str
    organization:str
    organizationalUnit:str
    domain:str
