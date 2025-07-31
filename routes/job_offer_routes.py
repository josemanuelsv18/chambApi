from fastapi import APIRouter, HTTPException
from controllers.job_offer_controller import JobOfferController
from schemas.job_offer import JobOfferResponse, JobOfferCreate, JobOfferUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection
from datetime import date

class JobOfferRoutes(BaseRoutes[JobOfferResponse, JobOfferCreate, JobOfferUpdate]):
    def __init__(self, conn: Connection):
        controller = JobOfferController(conn)
        super().__init__(controller, prefix="/job_offers", tags=["job_offers"])

        @self.router.post("/", response_model=bool)
        def create(item: JobOfferCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: JobOfferUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/with_company/all", response_model=list[dict])
        def get_all_job_offers_with_company():
            result = self.controller.get_all_job_offers_with_company()
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found")
            return result

        @self.router.get("/with_company/{job_offer_id}", response_model=dict)
        def get_job_offer_with_company(job_offer_id: int):
            result = self.controller.get_job_offer_with_company(job_offer_id)
            if not result:
                raise HTTPException(status_code=404, detail="Job offer not found")
            return result

        @self.router.get("/by_company/{company_id}", response_model=list[JobOfferResponse])
        def get_job_offers_by_company(company_id: int):
            result = self.controller.get_job_offers_by_company(company_id)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found for this company")
            return result

        @self.router.get("/by_title/{title}", response_model=list[JobOfferResponse])
        def get_job_offers_by_title(title: str):
            result = self.controller.get_job_offers_by_title(title)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this title")
            return result

        @self.router.get("/by_category/{category}", response_model=list[JobOfferResponse])
        def get_job_offers_by_category(category: str):
            result = self.controller.get_job_offers_by_category(category)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found in this category")
            return result

        @self.router.get("/by_start_date/{start_date}", response_model=list[JobOfferResponse])
        def get_job_offers_by_start_date(start_date: date):
            result = self.controller.get_job_offers_by_start_date(start_date)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this start date")
            return result

        @self.router.get("/all/by_status/{status}", response_model=list[JobOfferResponse])
        def get_all_job_offers_by_status(status: str):
            result = self.controller.get_all_job_offers_by_status(status)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this status")
            return result

def get_job_offer_routes(conn: Connection) -> APIRouter:
    return JobOfferRoutes(conn).router