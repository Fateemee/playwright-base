import pytest
import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from service.UserService import UserService
from model.queries.user.UserLoginQuery import UserLoginQuery

load_dotenv()

USERNAME = os.getenv("MY_USERNAME")
PASSWORD = os.getenv("MY_PASSWORD")

@pytest.mark.asyncio
async def test_login_api():
    async with async_playwright() as p:
        request_context = await p.request.new_context()
        user_service = UserService(request_context)

        login_query = UserLoginQuery(username=USERNAME, password=PASSWORD)
        await user_service.login_api(login_query)

        await request_context.dispose()
if __name__ == "__main__":
    asyncio.run(test_login_api())