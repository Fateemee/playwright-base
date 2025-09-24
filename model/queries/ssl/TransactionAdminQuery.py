from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class TransactionAdminQuery:
    limit: Optional[int] = None
    status: Optional[Dict] = None
    type: Optional[Dict] = None
    request: Optional[Dict] = None
    created_at: Optional[Dict] = None
    updated_at: Optional[Dict] = None
    id: Optional[Dict] = None
