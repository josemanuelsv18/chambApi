from fastapi import APIRouter, HTTPException
from controllers.user_controller import UserController
from schemas.user import UserResponse, UserCreate, UserUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class UserRoutes(BaseRoutes[UserResponse, UserCreate, UserUpdate]):
    def __init__(self, conn: Connection):
        controller = UserController(conn)
        super().__init__(controller, prefix="/users", tags=["users"])

        @self.router.post("/", response_model=bool)
        def create(item: UserCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: UserUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        # additional route definitions
        @self.router.get("/exists/email/{email}", response_model=bool)
        def exists_by_email(email: str):
            return self.controller.exists_by_email(email)

        @self.router.get("/exists/phone/{phone}", response_model=bool)
        def exists_by_phone(phone: str):
            return self.controller.exists_by_phone(phone)
        

def get_user_routes(conn: Connection) -> APIRouter:
    return UserRoutes(conn).router
    