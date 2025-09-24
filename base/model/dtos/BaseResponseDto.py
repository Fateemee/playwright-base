from dataclasses import dataclass
from typing import Optional

@dataclass
class BaseResponseDto:
    message: Optional[str] = None
