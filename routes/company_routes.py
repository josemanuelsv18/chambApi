from fastapi import APIRouter, HTTPException
from controllers.company_controller import CompanyController
from schemas.company import CompanyResponse, CompanyCreate, CompanyUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class CompanyRoutes(BaseRoutes[CompanyResponse, CompanyCreate, CompanyUpdate]):
    def __init__(self, conn: Connection):
        controller = CompanyController(conn)
        super().__init__(controller, prefix="/companies", tags=["companies"])

        @self.router.post("/", response_model=bool)
        def create(item: CompanyCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: CompanyUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/{company_id}/with_user", response_model=dict)
        def get_company_with_user(company_id: int):
            result = self.controller.get_company_with_user(company_id)
            if not result:
                raise HTTPException(status_code=404, detail="Company not found")
            return result
        
        @self.router.get("/{company_name}/by_name", response_model=dict)
        def get_company_by_name(company_name: str):
            result = self.controller.get_company_by_name(company_name)
            if not result:
                raise HTTPException(status_code=404, detail="Company not found")
            return result

        @self.router.get("/{business_type}/by_type", response_model=list[CompanyResponse])
        def get_company_by_type(business_type: str):
            result = self.controller.get_company_by_type(business_type)
            if not result:
                raise HTTPException(status_code=404, detail="No companies found")
            return result

        @self.router.get("/by_user/{user_id}", response_model=dict)
        def get_company_by_user_id(user_id: int):
            """
            Obtener una empresa (company) por su user_id.
            """
            try:
                with self.controller.conn.get_cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM companies WHERE user_id = %s LIMIT 1", (user_id,)
                    )
                    company = cursor.fetchone()
                    if not company:
                        raise HTTPException(status_code=404, detail="Company not found")
                    return company
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

def get_company_routes(conn: Connection) -> APIRouter:
    return CompanyRoutes(conn).router