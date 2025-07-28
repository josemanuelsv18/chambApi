from schemas.payment import PaymentCreate, PaymentUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
from enums.enums import PaymentStatus
import psycopg2

class PaymentController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('payments', conn)

    def create(self, payment_data: PaymentCreate) -> bool:
        data = payment_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s, %s)",
                    (
                        data['job_id'],
                        data['amount'],
                        data['payment_status'].value if data.get('payment_status') else None,
                        data['payment_method'],
                        data.get('payment_details'),
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"Payment created, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, payment_data: PaymentUpdate) -> bool:
        data = payment_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s)",
                    (
                        id,
                        data['payment_status'].value if data.get('payment_status') else None,
                        data.get('payment_details')
                    )
                )
                return True
        except psycopg2.Error as e:
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
        except psycopg2.Error as e:
            print(f"Error fetching payments by job: {e}")
            return []
        
    def get_payments_with_job_details(self, job_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT p.*, j.title, j.status, j.worker_id, j.application_id
                FROM payments p
                JOIN jobs j ON p.job_id = j.id
                WHERE p.job_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
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
        except psycopg2.Error as e:
            print(f"Error fetching payments by status: {e}")
            return []