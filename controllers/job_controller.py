from schemas.job import JobCreate, JobUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
from enums.enums import JobStatus

class JobController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('jobs', conn)

    def create(self, job_data: JobCreate) -> bool:
        data = job_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['job_offer_id'],
                    data['worker_id'],
                    data['application_id'],
                    data['title'],
                    data['job_status'].value if data.get('job_status') else None,
                    0
                ]
                cursor.callproc(f'sp_create_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, job_data: JobUpdate) -> bool:
        data = job_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('title'),
                    data['job_status'].value if data.get('job_status') else None
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_jobs_by_worker(self, worker_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM jobs
                WHERE worker_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (worker_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching jobs by worker: {e}")
            return []

    def get_jobs_by_status(self, status: JobStatus) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM jobs
                WHERE status = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (status.value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching jobs by status: {e}")
            return []
        
    def get_job_with_details(self, job_id: int) -> Optional[Dict[str, Any]]:
        try:
            # Fetch job details along with related job offer, worker, and application information
            query = """
                SELECT j.*, jo.title as job_offer_title, w.first_name as worker_first_name, a.application_status
                FROM jobs j
                JOIN job_offers jo ON j.job_offer_id = jo.id
                JOIN workers w ON j.worker_id = w.id
                JOIN applications a ON j.application_id = a.id
                WHERE j.id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching job with details: {e}")
            return None