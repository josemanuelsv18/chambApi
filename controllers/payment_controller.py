from ..schemas.payment import PaymentCreate, PaymentUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any
from ..enums.enums import PaymentStatus

class PaymentController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('payments', conn)

    def create(self, payment_data: PaymentCreate) -> int:
        data = payment_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['job_id'],
                    data['amount'],
                    data['payment_status'].value if data.get('payment_status') else None,
                    data['payment_method'],
                    data.get('payment_details'),
                    0  # OUT param para el id generado
                ]
                cursor.callproc(f'sp_create_{self.table_name}', args)
                self.conn.connection.commit()
                for result in cursor.stored_results():
                    new_id = result.fetchone()[0]
                return new_id
        except Exception as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return None

    def update(self, id: int, payment_data: PaymentUpdate) -> bool:
        data = payment_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data['payment_status'].value if data.get('payment_status') else None,
                    data.get('payment_details')
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_payments_by_job(self, job_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM payments
                WHERE job_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching payments by job: {e}")
            return []
        
    def get_payments_with_job_details(self, job_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT p.*, j.title, j.job_status, j.worker_id, j.application_id
                FROM payments p
                JOIN jobs j ON p.job_id = j.id
                WHERE p.job_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching payments with job details: {e}")
            return []

    def get_payments_by_status(self, status: PaymentStatus) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM payments
                WHERE status = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (status.value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching payments by status: {e}")
            return []