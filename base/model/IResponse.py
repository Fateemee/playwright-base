from dataclasses import dataclass
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

@dataclass
class IResponse(Generic[T]):
      data: T
      messages: Optional[List[str]] = None
      message: Optional[str] = None
      success: Optional[bool] = None
      status: Optional[int] = None
      error: Optional[str] = None

from enum import Enum

class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
