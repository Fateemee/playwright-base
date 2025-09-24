import os
from base.controller.BaseController import BaseController
from base.model.enums.Enum import HttpMethod
from base.constant.constant import VERSION1 , DOMAIN_ENTITY
from model.dtos.domain.DomainExistsDto import DomainExistsDto
from model.dtos.domain.DomainCheckDto import DomainCheckDto
from model.dtos.domain.IrnicIdNotHandleDto import IrnicIdNotHandleDto

class DomainController(BaseController):
    def __init__(self, request_context):
        super().__init__(
            request_context=request_context,
            base_url=os.environ.get("BASE_URL_develop"),
            version=VERSION1,
            entity=DOMAIN_ENTITY
        )

    async def domain_exists(self , query:str) -> DomainExistsDto:
        self.set_method(HttpMethod.GET)\
            .set_path(f"/{query}/exists")\

        full_response = await self.request(response_type=DomainExistsDto)
        return full_response.data
    
    async def domain_check(self , query:str) -> DomainCheckDto:
        self.set_method(HttpMethod.GET)\
            .set_path(f"/{query}/check")\

        full_response = await self.request(response_type=DomainCheckDto)
        return full_response.data
    
    async def valid_handelIrnicId(self , query) -> IrnicIdNotHandleDto:
        self.set_method(HttpMethod.GET)\
            .set_path(f"validate-handle/{query}/")\
            
        full_response = await self.request(response_type=IrnicIdNotHandleDto)
        print('tttttttttttttttttttttt', full_response.status)
        return full_response

