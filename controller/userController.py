import os
from base.controller.BaseController import BaseController
from base.model.enums.Enum import HttpMethod
from base.constant.constant import VERSION1, USER_ENTITY
from model.queries.user.UserLoginQuery import UserLoginQuery
from model.dtos.user.UserLoginDto import UserLoginDto

class UserController(BaseController):
    def __init__(self, request_context):
        super().__init__(
            request_context=request_context,
            base_url=os.environ.get("BASE_URL_develop"),
            version=VERSION1,
            entity=USER_ENTITY
        )

    async def login(self, login_query: UserLoginQuery) -> UserLoginDto:
        self.set_method(HttpMethod.POST)\
            .set_path("login")\
            .set_body(login_query.__dict__)

        full_response = await self.request(response_type=UserLoginDto)
        return full_response.data
