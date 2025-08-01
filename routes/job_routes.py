from fastapi import APIRouter, HTTPException
from controllers.job_controller import JobController
from schemas.job import JobResponse, JobCreate, JobUpdate, JobSimpleResponse
from routes.base_routes import BaseRoutes
from database.connection import Connection

class JobRoutes(BaseRoutes[JobResponse, JobCreate, JobUpdate]):
    def __init__(self, conn: Connection):
        controller = JobController(conn)
        super().__init__(controller, prefix="/jobs", tags=["jobs"])

        @self.router.post("/", response_model=bool)
        def create(item: JobCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: JobUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/{job_id}/details", response_model=dict)
        def get_job_with_details(job_id: int):
            result = self.controller.get_job_with_details(job_id)
            if not result:
                raise HTTPException(status_code=404, detail="Job not found")
            return result

        @self.router.get("/{worker_id}/worker", response_model=list[JobSimpleResponse])
        def get_jobs_by_worker(worker_id: int):
            jobs = self.controller.get_jobs_by_worker(worker_id)
            if not jobs:
                raise HTTPException(status_code=404, detail="No jobs found for this worker")
            return jobs 
        
        @self.router.get("/{status}/by_status", response_model=list[JobResponse])
        def get_jobs_by_status(status: str):
            jobs = self.controller.get_jobs_by_status(status)
            if not jobs:
                raise HTTPException(status_code=404, detail="No jobs found with this status")
            return jobs

def get_job_routes(conn: Connection) -> APIRouter:
    return JobRoutes(conn).router