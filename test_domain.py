import pytest
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from service.DomainService import DomainService
from helper.DBHelper import DBHelper 

load_dotenv()
@pytest.mark.asyncio
async def test_domain():
    async with async_playwright() as JOKERdomainNotexistindomainmodule:
        request_context = await JOKERdomainNotexistindomainmodule.request.new_context()
        domain_service = DomainService(request_context)
        #db_multi = DBHelper("multi")
        #row_multi = await db_multi.fetch_one("SELECT * from domains LIMIT 1;")
        #print("✅ row_multi:", row_multi)
        domain = 'childnstest1.com'
        response = await domain_service.valid_domain_exists(domain , False)
        print("✅ JOKERdomainNotexistindomainmodule:", response.exists)
        await request_context.dispose()
    

    async with async_playwright() as JOKERdomainexistindomainmodule:
        request_context = await JOKERdomainexistindomainmodule.request.new_context()
        domain_service = DomainService(request_context)
        domain = 'childnstest.com'
        response = await domain_service.valid_domain_exists(domain ,True)
        print("✅ JOKERdomainexistindomainmodule:", response.exists)
        await request_context.dispose()

    async with async_playwright() as IrnicdomainNOtexistindomainmodule:
        request_context = await IrnicdomainNOtexistindomainmodule.request.new_context()
        domain_service = DomainService(request_context)
        domain = 'childnstestirnic.ir'
        response = await domain_service.valid_domain_exists(domain ,False)
        print("✅ IrnicdomainNOtexistindomainmodule:", response.exists)
        await request_context.dispose()


    async with async_playwright() as domainIsPremiumandAvailable:
        request_context = await domainIsPremiumandAvailable.request.new_context()
        domain_service = DomainService(request_context)
        domain = 'new.gift'
        response = await domain_service.domain_check(domain ,True ,True)
        await request_context.dispose()

    async with async_playwright() as domainIsPremiumandInUse:
        request_context = await domainIsPremiumandInUse.request.new_context()
        domain_service = DomainService(request_context)
        domain = 'pango.co'
        response = await domain_service.domain_check(domain ,False ,True)
        await request_context.dispose()

    async with async_playwright() as handelIrnicIdَAPi_IDInIranserver:
        request_context = await handelIrnicIdَAPi_IDInIranserver.request.new_context()
        domain_service = DomainService(request_context)
        notValidIrnicIds = ['greenwebdomains@iranserver.com' , 'mm61-irnic','gr62-irnic']
        response = await domain_service.valid_handle_IrnicId(notValidIrnicIds)
        await request_context.dispose()

if __name__ == "__main__":
    asyncio.run(test_domain())
