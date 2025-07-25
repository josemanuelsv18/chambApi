from fastapi import APIRouter, HTTPException
from controllers.admin_controller import AdminController
from schemas.admin import AdminResponse, AdminCreate, AdminUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class AdminRoutes(BaseRoutes[AdminResponse, AdminCreate, AdminUpdate]):
    def __init__(self, conn: Connection):
        controller = AdminController(conn)
        super().__init__(controller, prefix="/admins", tags=["admins"])

        @self.router.post("/", response_model=bool)
        def create(item: AdminCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: AdminUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/{admin_id}/with_user", response_model=dict)
        def get_admin_with_user(admin_id: int):
            result = self.controller.get_admin_with_user(admin_id)
            if not result:
                raise HTTPException(status_code=404, detail="Admin not found")
            return result

def get_admin_routes(conn: Connection) -> APIRouter:
    return AdminRoutes(conn).router