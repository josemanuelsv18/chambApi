from fastapi import APIRouter, HTTPException
from ..controllers.company_controller import CompanyController
from ..schemas.company import CompanyResponse, CompanyCreate, CompanyUpdate
from .base_routes import BaseRoutes
from ..database.connection import Connection

class CompanyRoutes(BaseRoutes[CompanyResponse, CompanyCreate, CompanyUpdate]):
    def __init__(self, conn: Connection):
        controller = CompanyController(conn)
        super().__init__(controller, prefix="/companies", tags=["companies"])

        @self.router.get("/{company_id}/with_user", response_model=dict)
        def get_company_with_user(company_id: int):
            result = self.controller.get_company_with_user(company_id)
            if not result:
                raise HTTPException(status_code=404, detail="Company not found")
            return result

def get_company_routes(conn: Connection) -> APIRouter:
    return CompanyRoutes(conn).router