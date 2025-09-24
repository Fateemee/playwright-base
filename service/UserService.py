from controller.userController import UserController
from model.queries.user.UserLoginQuery import UserLoginQuery
from model.dtos.user.UserLoginDto import UserLoginDto
from service.auth_manager import AuthManager

class UserService:
    def __init__(self, request_context):
        self.user_controller = UserController(request_context)

    async def login_api(self, login_query: UserLoginQuery) -> UserLoginDto:
        response = await self.user_controller.login(login_query)
        
        assert response is not None, "Login response is  not None"
        assert response.access_token, "Access token is "
        assert isinstance(response.expires_in, int), "expires_in should be int"

        AuthManager.set_token(response.access_token)
        #print("✅ Login success. Access token:", response.access_token)
        return response