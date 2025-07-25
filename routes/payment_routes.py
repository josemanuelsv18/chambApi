from fastapi import APIRouter, HTTPException
from controllers.payment_controller import PaymentController
from schemas.payment import PaymentResponse, PaymentCreate, PaymentUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class PaymentRoutes(BaseRoutes[PaymentResponse, PaymentCreate, PaymentUpdate]):
    def __init__(self, conn: Connection):
        controller = PaymentController(conn)
        super().__init__(controller, prefix="/payments", tags=["payments"])

        @self.router.get("/{job_id}/by-job", response_model=list[PaymentResponse])
        def get_payments_by_job(job_id: int):
            payments = controller.get_payments_by_job(job_id)
            if not payments:
                raise HTTPException(status_code=404, detail="No payments found for this job")
            return payments
        
        @self.router.get("/{job_id}/with_details", response_model=list[PaymentResponse])
        def get_payments_with_job_details(job_id: int):
            payments = controller.get_payments_by_job(job_id)
            if not payments:
                raise HTTPException(status_code=404, detail="No payments found for this job")
            return payments
        
        @self.router.get("/{status}/by_status", response_model=list[PaymentResponse])
        def get_payments_by_status(status: str):
            payments = controller.get_payment_by_status(status)
            if not payments:
                raise HTTPException(status_code=404, detail="No payments found with this status")
            return payments

        @self.router.post("/", response_model=bool)
        def create(item: PaymentCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: PaymentUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

def get_payment_routes(conn: Connection) -> APIRouter:
    return PaymentRoutes(conn).router