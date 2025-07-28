from schemas.application import ApplicationCreate, ApplicationUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
import psycopg2

class ApplicationController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('applications', conn)

    def create(self, application_data: ApplicationCreate) -> bool:
        data = application_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s, %s)",
                    (
                        data['job_offer_id'],
                        data['worker_id'],
                        data['application_status'].value if data.get('application_status') else None,
                        data['applied_at'],
                        data.get('message'),
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"Application created, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, application_data: ApplicationUpdate) -> bool:
        data = application_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s, %s, %s)",
                    (
                        id,
                        data['application_status'].value if data.get('application_status') else None,
                        data.get('message'),
                        data.get('company_response'),
                        data.get('response_at')
                    )
                )
                return True
        except psycopg2.Error as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_applications_by_worker(self, worker_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM applications
                WHERE worker_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (worker_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching applications by worker: {e}")
            return []

    def get_applications_by_job_offer(self, job_offer_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM applications
                WHERE job_offer_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_offer_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching applications by job offer: {e}")
            return []