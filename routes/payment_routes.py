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

def get_payment_routes(conn: Connection) -> APIRouter:
    return PaymentRoutes(conn).router