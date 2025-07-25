from ..schemas.job_offer import JobOfferCreate, JobOfferUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any
from ..enums.enums import JobCategory, ExperienceLevel, JobOfferStatus
from datetime import date

class JobOfferController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('job_offers', conn)

    def create(self, job_offer_data: JobOfferCreate) -> int:
        data = job_offer_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['company_id'],
                    data['title'],
                    data['description'],
                    data['category'],
                    data['location'],
                    data['start_date'],
                    data['end_date'],
                    data['start_time'],
                    data['end_time'],
                    data['required_workers'],
                    data['hourly_rate'],
                    data['total_payment'],
                    data['experience_level'].value if data.get('experience_level') else None,
                    data['job_status'].value if data.get('job_status') else None,
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

    def update(self, id: int, job_offer_data: JobOfferUpdate) -> bool:
        data = job_offer_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('title'),
                    data.get('description'),
                    data.get('category'),
                    data.get('location'),
                    data.get('start_date'),
                    data.get('end_date'),
                    data.get('start_time'),
                    data.get('end_time'),
                    data.get('required_workers'),
                    data.get('hourly_rate'),
                    data.get('total_payment'),
                    data['experience_level'].value if data.get('experience_level') else None,
                    data['job_status'].value if data.get('job_status') else None,
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_job_offer_with_company(self, job_offer_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT j.*, c.company_name, c.business_type, c.logo
                FROM job_offers j
                JOIN companies c ON j.company_id = c.id
                WHERE j.id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_offer_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching job offer with company: {e}")
            return None

    def get_job_offers_by_company(self, company_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE company_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (company_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching job offers by company: {e}")
            return []

    def get_job_offer_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE title = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (title,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching job offer by title: {e}")
            return None
        
    def get_job_offers_by_category(self, category: JobCategory) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE category = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (category.value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching job offers by category: {e}")
            return []
        
    def get_job_by_start_date(self, date: date) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE start_date = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (date,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching job offers by start date: {e}")
            return []
        
    def get_job_by_experience_level(self, experience_level: ExperienceLevel) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE experience_level = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (experience_level.value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching job offers by experience level: {e}")
            return []
        
    def get_all_job_offers_by_status(self, status: JobOfferStatus) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM job_offers
                WHERE job_status = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (status.value,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching job offers by status: {e}")
            return []