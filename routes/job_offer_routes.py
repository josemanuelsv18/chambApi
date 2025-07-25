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

        @self.router.get("/{job_offer_id}/with_company", response_model=dict)
        def get_job_offer_with_company(job_offer_id: int):
            result = self.controller.get_job_offer_with_company(job_offer_id)
            if not result:
                raise HTTPException(status_code=404, detail="Job offer not found")
            return result

        @self.router.get("/{company_id}/by_company", response_model=list[JobOfferResponse])
        def get_job_offers_by_company(company_id: int):
            result = self.controller.get_job_offers_by_company(company_id)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found for this company")
            return result
    
        @self.router.get("/{title}/by_title", response_model=list[JobOfferResponse])
        def get_job_offers_by_title(title: str):
            result = self.controller.get_job_offers_by_title(title)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this title")
            return result
        
        @self.router.get("/{category}/by_category", response_model=list[JobOfferResponse])
        def get_job_offers_by_category(category: str):
            result = self.controller.get_job_offers_by_category(category)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found in this category")
            return result
        
        @self.router.get("/{start_date}/by_start_date", response_model=list[JobOfferResponse])
        def get_job_offers_by_start_date(start_date: date):
            result = self.controller.get_job_offers_by_start_date(start_date)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this start date")
            return result

        @self.router.get("/all/{status}/by_status", response_model=list[JobOfferResponse])
        def get_all_job_offers_by_status(status: str):
            result = self.controller.get_all_job_offers_by_status(status)
            if not result:
                raise HTTPException(status_code=404, detail="No job offers found with this status")
            return result

def get_job_offer_routes(conn: Connection) -> APIRouter:
    return JobOfferRoutes(conn).router