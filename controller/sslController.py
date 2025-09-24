import os
from base.controller.BaseController import BaseController
from base.model.IResponse import IResponse
from base.model.enums.Enum import HttpMethod
from base.constant.constant import VERSION1 , CSR_ENTITY , SSL_ENTITY,SSLADMIN_ENTITY
from model.dtos.ssl.TransactionAdminDto import TransactionAdminDto
from model.dtos.ssl.GenerateCsrDtos import GenerateCsrDto
from model.commands.ssl.GenerateCsrCommand import GenerateCsrCommand
from model.dtos.ssl.CheckCsrDtos import CheckCsrDto
from model.commands.ssl.CheckCsrCommand import CheckCsrCommand
from model.commands.ssl.CreateSslCommand import CreateSslCommand
from model.dtos.ssl.CreateSslDto import CreateSslDto
from model.commands.ssl.CancelSslCommand import CancelSslCommand
from model.dtos.ssl.CancelSslDto import CancelSsslDto
from dataclasses import asdict
from urllib.parse import urlencode

from model.queries.ssl.TransactionAdminQuery import TransactionAdminQuery

class SSLController(BaseController):
    def __init__(self, request_context):
        super().__init__(
            request_context=request_context,
            base_url=os.environ.get("BASE_URL_develop"),
            version=VERSION1,
            entity=CSR_ENTITY
        )

    async def generate_csr(self, command: GenerateCsrCommand) -> GenerateCsrDto:
        self.set_method(HttpMethod.POST)\
            .set_path("generate")\
            .set_body(command.__dict__)

        full_response = await self.request(response_type=GenerateCsrDto)
        return full_response.data

    async def check_csr(self, command: CheckCsrCommand) -> CheckCsrDto:
        self.set_method(HttpMethod.POST)\
            .set_path("checker")\
            .set_body(command.__dict__)

        full_response = await self.request(response_type=CheckCsrDto)
        return full_response.data   
    
    async def create_ssl(self, command: CreateSslCommand) -> IResponse[CreateSslDto]:
        self.entity = SSL_ENTITY
        self.set_method(HttpMethod.POST)\
            .set_path("")\
            .set_body(asdict(command))
        full_response = await self.request(response_type=CreateSslDto)
        return full_response

    async def cancel_ssl_transaction(self, command: CancelSslCommand, use_query: bool = False) -> CancelSsslDto:
        self.entity = SSLADMIN_ENTITY
        self.set_admin_token()
        self.set_method(HttpMethod.DELETE).set_path("transaction")

        if use_query:
            self.set_query(command.__dict__)
            full_response = await self.request(
                response_type=CancelSsslDto
            )
        else:
            body_encoded = urlencode(command.__dict__)
            full_response = await self.request(
                response_type=CancelSsslDto,
                body_str=body_encoded,
                content_type="application/x-www-form-urlencoded"
            )

        return full_response
    
    async def admin_transaction(self, query: TransactionAdminQuery) -> TransactionAdminDto:
        self.entity = SSLADMIN_ENTITY
        self.set_admin_token()
        self.set_method(HttpMethod.GET)\
            .set_path("transaction")\
            .set_query(query.__dict__)

        full_response = await self.request(response_type=TransactionAdminDto)
        if full_response.status != 200:
            raise Exception(f"Tranasction SSL failed: {full_response.message}")
        else:
            assert full_response.status ==200
        return full_response.data