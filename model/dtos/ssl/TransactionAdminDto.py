from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class RequesterDto:
    email: str
    firstName: str
    lastName: str
    phone: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class SslDto:
    certificate_id: Optional[str]
    created_at: Optional[str]
    csr: Optional[str]
    deleted_at: Optional[str]
    domain: Optional[str]
    expired_at: Optional[str]
    id: Optional[int]
    order_id: Optional[str]
    period: Optional[str]
    provider: Optional[str]
    reissued_at: Optional[str]
    status: Optional[str]
    type: Optional[str]
    updated_at: Optional[str]
    user_id: Optional[int]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class RequestDto:
    admin_id: Optional[Any]
    csr: str
    days_left_expiration: Optional[int]
    domain: str
    job_execution_date: Optional[str]
    method: str
    prefix: Optional[str]
    product: Optional[str]
    provider: str
    requester: Optional[RequesterDto]
    ssl: Optional[SslDto]
    user_id: int

    @classmethod
    def from_dict(cls, data: dict):
        requester = RequesterDto.from_dict(data["requester"]) if "requester" in data else None
        ssl = SslDto.from_dict(data["ssl"]) if data.get("ssl") else None
        return cls(
            admin_id=data.get("admin_id"),
            csr=data.get("csr"),
            days_left_expiration=data.get("days_left_expiration"),
            domain=data.get("domain"),
            job_execution_date=data.get("job_execution_date"),
            method=data.get("method"),
            prefix=data.get("prefix"),
            product=data.get("product"),
            provider=data.get("provider"),
            requester=requester,
            ssl=ssl,
            user_id=data.get("user_id"),
        )


@dataclass
class ResponseItemDto:
    new_order_id: Optional[str] = None
    order_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            new_order_id=data.get("new_order_id"),
            order_id=data.get("order_id"),
        )


@dataclass
class DataItemDto:
    attempt: int
    created_at: Optional[str]
    domain: str
    id: int
    order_id: Optional[str]
    request: Optional[RequestDto]
    response: Optional[List[ResponseItemDto]]
    status: str
    type: str
    updated_at: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        request = RequestDto.from_dict(data["request"]) if "request" in data else None
        response = [ResponseItemDto.from_dict(r) for r in data.get("response", [])] if data.get("response") else None
        return cls(
            attempt=data.get("attempt"),
            created_at=data.get("created_at"),
            domain=data.get("domain"),
            id=data.get("id"),
            order_id=data.get("order_id"),
            request=request,
            response=response,
            status=data.get("status"),
            type=data.get("type"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class TransactionAdminDto:
    data: List[DataItemDto] = field(default_factory=list)

    def __getitem__(self, idx: int) -> DataItemDto:
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    @classmethod
    def from_list(cls, data_list: list):
        parsed_data = [DataItemDto.from_dict(item) for item in data_list]
        return cls(data=parsed_data)
    
    def first(self) -> DataItemDto:
        if not self.data:
            raise ValueError("TransactionAdminDto.data is empty")
        return self.data[0]
