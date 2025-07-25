from fastapi import APIRouter, HTTPException
from ..controllers.worker_controller import WorkerController
from ..schemas.worker import WorkerResponse, WorkerCreate, WorkerUpdate
from .base_routes import BaseRoutes
from ..database.connection import Connection

class WorkerRoutes(BaseRoutes[WorkerResponse, WorkerCreate, WorkerUpdate]):
    def __init__(self, conn: Connection):
        controller = WorkerController(conn)
        super().__init__(controller, prefix="/workers", tags=["workers"])

        # Ruta adicional para obtener worker junto con datos de usuario
        @self.router.get("/{worker_id}/with_user", response_model=dict)
        def get_worker_with_user(worker_id: int):
            result = self.controller.get_worker_with_user(worker_id)
            if not result:
                raise HTTPException(status_code=404, detail="Worker not found")
            return result

def get_worker_routes(conn: Connection) -> APIRouter:
    return WorkerRoutes(conn).router