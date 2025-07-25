from fastapi import APIRouter, HTTPException
from controllers.application_controller import ApplicationController
from schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class ApplicationRoutes(BaseRoutes[ApplicationResponse, ApplicationCreate, ApplicationUpdate]):
    def __init__(self, conn: Connection):
        controller = ApplicationController(conn)
        super().__init__(controller, prefix="/applications", tags=["applications"])

        @self.router.get("/by_worker/{worker_id}", response_model=list)
        def get_applications_by_worker(worker_id: int):
            return self.controller.get_applications_by_worker(worker_id)

        @self.router.get("/by_job_offer/{job_offer_id}", response_model=list)
        def get_applications_by_job_offer(job_offer_id: int):
            return self.controller.get_applications_by_job_offer(job_offer_id)

def get_application_routes(conn: Connection) -> APIRouter:
    return ApplicationRoutes(conn).router