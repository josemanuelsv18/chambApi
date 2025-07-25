from ..schemas.application import ApplicationCreate, ApplicationUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any

class ApplicationController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('applications', conn)

    def create(self, application_data: ApplicationCreate) -> int:
        data = application_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['job_offer_id'],
                    data['worker_id'],
                    data['application_status'].value if data.get('application_status') else None,
                    data['applied_at'],
                    data.get('message'),
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

    def update(self, id: int, application_data: ApplicationUpdate) -> bool:
        data = application_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data['application_status'].value if data.get('application_status') else None,
                    data.get('message'),
                    data.get('company_response'),
                    data.get('response_at')
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            print(f"Error fetching applications by job offer: {e}")
            return []

    def get_application_by_worker_id(self, worker_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM applications
                WHERE worker_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (worker_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching application by worker ID: {e}")
            return None