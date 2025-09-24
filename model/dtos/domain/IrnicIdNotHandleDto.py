from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ErrorDetailsDto:
    handle: List[str]  # چون توی details → handle یه لیست از استرینگه


@dataclass
class ErrorDto:
    message: str
    details: ErrorDetailsDto
    msgType: str


@dataclass
class IrnicIdNotHandleDto:
    error: ErrorDto
