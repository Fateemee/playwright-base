from base.model.IResponse import IResponse
from model.commands.ssl.GenerateCsrCommand import GenerateCsrCommand
from model.commands.ssl.CreateSslCommand import CreateSslCommand, Requester
from model.commands.ssl.CancelSslCommand import CancelSslCommand
from model.dtos.ssl.TransactionAdminDto import TransactionAdminDto
from model.dtos.ssl.CreateSslDto import CreateSslDto
from model.dtos.ssl.CancelSslDto import CancelSsslDto
from controller.sslController import SSLController
from model.queries.ssl.TransactionAdminQuery import TransactionAdminQuery
from enums.SslStausType import SslStatusType
import asyncio
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)


class SSLService:
    def __init__(self, request_context):
        self.ssl_controller = SSLController(request_context)

    async def generate_and_check_csr(self, command: GenerateCsrCommand):
        response = await self.ssl_controller.generate_csr(command)
        assert response is not None, "CSR response is None"
        assert hasattr(response, "csr") and response.csr, "CSR is missing"
        return response, True

    async def createSsl(self, command: CreateSslCommand) -> IResponse[CreateSslDto]:
        sslCreateResponse = await self.ssl_controller.create_ssl(command)
        transaction_id = getattr(sslCreateResponse.data, "transaction_id", None)
        message = getattr(sslCreateResponse.data, "message", "")

        if sslCreateResponse.status == 200:
            assert sslCreateResponse is not None, "Response from Create Ssl is None"
            assert message == "گواهی مورد نظر در صف ایجاد قرار گرفت", f"Unexpected message: {message}"
            assert transaction_id is not None, "transaction_id is None"
            assert isinstance(transaction_id, int), f"transaction_id is not int: {transaction_id}"
            print("✅ message: ", message)
            print("✅ transaction_id: ", transaction_id)
        else:
            assert sslCreateResponse.status == 422
            print("⚠️ Create SSL Error:", message)
            print("status code :", sslCreateResponse.status)

        return sslCreateResponse

    async def cancelSslTransaction(self, command: CancelSslCommand, action: str) -> CancelSsslDto:
        response = await self.ssl_controller.cancel_ssl_transaction(command)
        print('cancelSslTransaction: ',response)
        if response.status != 200:
            raise Exception(f"Cancel SSL failed: {response.message}")
        cancel_data = response.data
        assert cancel_data is not None, "Cancel SSL data is None"
        assert cancel_data.action == action
        assert cancel_data.order_id is not None
        return cancel_data
    
    async def tranasctionAdminIndex(self, query: TransactionAdminQuery) -> TransactionAdminDto:
        response_list = await self.ssl_controller.admin_transaction(query)
        TransactionAdminDto.from_list(response_list)
        transaction_dto = TransactionAdminDto.from_list(response_list)
        first_item = transaction_dto.first()
        expected_id = query.id.get("value") if isinstance(query.id, dict) else query.id
        assert str(first_item.id) == str(expected_id), f"Expected id {expected_id}, got {first_item.id}"
        logging.info(f"Checking SSL TransactionId: {first_item.id}")
        max_retry = 40
        interval = 1  
        for _ in range(max_retry):
            first_item = transaction_dto.first()
            if first_item.status != SslStatusType.NEW:
                break
            await asyncio.sleep(interval)
        else:
            raise AssertionError(f"SSL status is still NEW after {max_retry*interval} seconds")

        assert first_item.status == SslStatusType.PENDING, f"Expected status PENDING, got {first_item.status}"    
        logging.info(f"Checking SSL status: {first_item.status}")   
        return response_list

        
        

