from playwright.async_api import APIRequestContext, APIResponse
from service.auth_manager import AuthManager
from base.model.enums.Enum import HttpMethod
from base.model.IResponse import IResponse
from typing import Optional, TypeVar, Generic, Type, cast
import json
import os

T = TypeVar("T")

class BaseController(Generic[T]):
    def __init__(
        self,
        request_context: APIRequestContext,
        base_url: str,
        version: str,
        entity: str
    ):
        self.request_context = request_context
        self.base_url = base_url.rstrip('/')
        self.version = version.strip('/')
        self.entity = entity.strip('/')
        self.method: HttpMethod = HttpMethod.GET
        self.path: Optional[str] = None
        self.body: Optional[dict] = None
        self.queries: Optional[dict] = None
        self.headers: dict = {}
        self.use_admin_token: bool = False  # تعیین نوع توکن

    def set_method(self, method: HttpMethod) -> "BaseController[T]":
        self.method = method
        return self

    def set_path(self, path: str) -> "BaseController[T]":
        self.path = path.strip('/')
        return self

    def set_body(self, body: dict) -> "BaseController[T]":
        self.body = body
        return self

    # def set_query(self, queries: dict) -> "BaseController[T]":
    #     self.queries = queries
    #     return self

    def set_query(self, queries: dict) -> "BaseController[T]":
        encoded_queries = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else v
            for k, v in queries.items()
            if v not in (None, "", {}, [])
        }
        self.queries = encoded_queries
        return self

    
    def set_admin_token(self):
        self.use_admin_token = True
        admin_token = os.getenv("ADMIN_TOKEN")
        if not admin_token:
            raise ValueError("ADMIN_TOKEN is not set in env")
        self.headers['Authorization'] = f"Bearer {admin_token}"

    def build_url(self) -> str:
        url = f"{self.base_url}"
        if self.version:
            url += f"/{self.version}"
        if self.entity:
            url += f"/{self.entity}"
        if self.path:
            url += f"/{self.path}"
        if self.queries:
            query_str = '&'.join([f"{k}={v}" for k, v in self.queries.items()])
            url += f"?{query_str}"
        return url

    async def request(
        self, 
        response_type: Optional[Type[T]] = None,
        body_str: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> IResponse[T]:
        
        if not self.use_admin_token:
            token = AuthManager.get_token()
            if token:
                self.headers['Authorization'] = f"Bearer {token}"

        self.headers['Content-Type'] = content_type if content_type else 'application/json'

        url = self.build_url()
        if body_str is not None:
            data_to_send = body_str
        elif self.body is not None:
            data_to_send = json.dumps(self.body)
        else:
            data_to_send = None

        # print("==== DEBUG REQUEST ====")
        # print("URL:", url)
        # print("Method:", self.method.value)
        # print("Headers:", self.headers)
        # print("Body:", data_to_send)
        # print("=======================")

        response: APIResponse = await self.request_context.fetch(
            url, 
            method=self.method.value,
            headers=self.headers,
            data=data_to_send
        )

        status = response.status
        response_json = await response.json()

        # print("==== DEBUG RESPONSE ====")
        # print("Status:", status)
        # print("Response JSON/Text:", response_json)
        # print("========================")

        iresponse = IResponse[T](
            data=None,
            messages=response_json.get("messages"),
            message=response_json.get("message"),
            success=response_json.get("success"),
            status=status
        )

        if status not in (200, 201, 204, 400):
            iresponse.message = f"Unexpected status code: {status}, response: {response_json}"
            return iresponse

        raw_data = response_json.get("data")
        if raw_data is None:
            if "errors" in response_json:
                iresponse.message = f"API Validation Error: {response_json['errors']}"
            elif "message" in response_json:
                iresponse.message = f"API Message: {response_json['message']}"
            return iresponse

        if response_type is not None:
            try:
                if isinstance(raw_data, dict):
                    filtered_data = {
                        k: v for k, v in raw_data.items()
                        if hasattr(response_type, "__annotations__") and k in response_type.__annotations__
                    }
                    iresponse.data = response_type(**filtered_data)
                else:
                    iresponse.data = cast(T, raw_data)
            except Exception as e:
                iresponse.message = f"[Warning] Failed to construct response_type model: {e}"
                iresponse.data = None
        else:
            iresponse.data = cast(T, raw_data)

        return iresponse
