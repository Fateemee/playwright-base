from dataclasses import dataclass

@dataclass
class CreateSslDto:
    message:str
    transaction_id:int