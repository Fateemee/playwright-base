from dataclasses import dataclass
from typing import Optional

@dataclass
class CancelSsslDto:
    action:str
    order_id:str