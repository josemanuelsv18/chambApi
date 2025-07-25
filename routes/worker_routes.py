from fastapi import APIRouter, HTTPException
from controllers.worker_controller import WorkerController
from schemas.worker import WorkerResponse, WorkerCreate, WorkerUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class WorkerRoutes(BaseRoutes[WorkerResponse, WorkerCreate, WorkerUpdate]):
    def __init__(self, conn: Connection):
        controller = WorkerController(conn)
        super().__init__(controller, prefix="/workers", tags=["workers"])

        @self.router.post("/", response_model=bool)
        def create(item: WorkerCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: WorkerUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/{worker_id}/with_user", response_model=dict)
        def get_worker_with_user(worker_id: int):
            result = self.controller.get_worker_with_user(worker_id)
            if not result:
                raise HTTPException(status_code=404, detail="Worker not found")
            return result

def get_worker_routes(conn: Connection) -> APIRouter:
    return WorkerRoutes(conn).router