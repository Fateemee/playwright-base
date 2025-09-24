from controller.domainController import DomainController
from model.dtos.domain.DomainExistsDto import DomainExistsDto
from model.dtos.domain.DomainCheckDto import DomainCheckDto
from model.dtos.domain.IrnicIdNotHandleDto import IrnicIdNotHandleDto
from model.dtos.domain.IrnicIdNotHandleDto import ErrorDto
from model.dtos.domain.IrnicIdNotHandleDto import ErrorDetailsDto

class DomainService:
    def __init__(self, request_context):
        self.domain_controller = DomainController(request_context)
    
    async def valid_domain_exists(self, query: str, should_exist: bool) -> DomainExistsDto:
        response = await self.domain_controller.domain_exists(query)
        assert response is not None
        assert response.exists is should_exist, f"Expected exists = {should_exist}, got {response.exists}"
        return response

    async def domain_check(self, query: str, available: bool , premium:bool) -> DomainCheckDto:
        response = await self.domain_controller.domain_check(query)
        assert response is not None
        assert response.available is available, f"Expected available = {available}, got {response.available}"
        assert response.premium is premium, f"Expected available = {premium}, got {response.premium}"
        if response.reason and not available:
            assert response.reason == "In use", f"Expected reason = 'In use', got '{response.reason}'"
            print("✅ domainIsPremiumandAvailable:", response.domain)
            print("✅ domainIsPremiumandInUse:", response.premium)
            print("✅ domainIsPremiumandInUse:", response.reason)
        else:
            print("✅ domainIsPremiumandAvailable:", response.domain)
            print("✅ domainIsPremiumandInUse:", response.premium)
            print("✅ domainIsPremiumandInUse:", response.reason)

        return response
    

    async def valid_handle_IrnicId(self, notValidIrnicIds: list[str]) -> IrnicIdNotHandleDto:
        for irnic_id in notValidIrnicIds:
            print(irnic_id)
            response = await self.domain_controller.valid_handelIrnicId(irnic_id)     
            print(response.error)
            
            #print(f"✅ {irnic_id} -> {response.error.details.handle[0]}")

        return response

            
