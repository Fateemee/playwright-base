import pytest
import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from model.commands.ssl.GenerateCsrCommand import GenerateCsrCommand
from model.commands.ssl.CreateSslCommand import CreateSslCommand, Requester
from model.commands.ssl.CancelSslCommand import CancelSslCommand
from model.queries.ssl.TransactionAdminQuery import TransactionAdminQuery
from service.SslService import SSLService
from service.UserService import UserService
from model.queries.user.UserLoginQuery import UserLoginQuery
from enums.SslJobType import SsLJobType

load_dotenv()

@pytest.mark.asyncio
async def test_ssl():
    # --- generate CSR ---
    async with async_playwright() as p:
        request_context = await p.request.new_context()
        ssl_service = SSLService(request_context)
        generate_command = GenerateCsrCommand(
            country="IR",
            state="Tehran",
            locality="Tehran",
            organization="green",
            organizationalUnit="product",
            domain="sslcreateftmtstauto.com"
        )
        generate_response, _ = await ssl_service.generate_and_check_csr(generate_command)
        await request_context.dispose()

    # --- create SSL ---
    async with async_playwright() as createSsl:
        request_context = await createSsl.request.new_context()
        ssl_service = SSLService(request_context)
        user_service = UserService(request_context)

        login_query = UserLoginQuery(
            username=os.getenv("MY_USERNAME_develop"),
            password=os.getenv("MY_PASSWORD_develop")
        )
        await user_service.login_api(login_query)

        create_command = CreateSslCommand(
            csr=generate_response.csr,
            domain=generate_command.domain,
            provider=os.getenv("SSL_PROVIDER"),
            san="",
            method="admin",
            product=601,
            username="",
            requester=Requester(
                firstName="fatemeh",
                lastName="mosavi",
                email=os.getenv("MY_USERNAME_develop"),
                phone=os.getenv("MY_PHONE")
            )
        )
        create_response = await ssl_service.createSsl(create_command)

    async with async_playwright() as adminTranasction:
        request_context = await adminTranasction.request.new_context()
        ssl_service = SSLService(request_context)
        if create_response.status == 200 and \
           getattr(create_response.data, "transaction_id", create_response.data.transaction_id) and \
           getattr(create_response.data, "message", "") == "گواهی مورد نظر در صف ایجاد قرار گرفت":
            
            tranaction_query=TransactionAdminQuery(
                id={"type":"exec","value":create_response.data.transaction_id}
            )
            tranaction_response = await ssl_service.tranasctionAdminIndex(tranaction_query)
            cancel_command = CancelSslCommand(
                domain=create_command.domain,
                type=SsLJobType.CREATE_ORDER,
                provider=os.getenv("SSL_PROVIDER")
            )
            cancel_response = await ssl_service.cancelSslTransaction(cancel_command, "Cancel")
            print("✅ SSL cancelled:", cancel_response)

        await request_context.dispose()   



if __name__ == "__main__":
    asyncio.run(test_ssl())
