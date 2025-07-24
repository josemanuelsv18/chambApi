from ..schemas.company import CompanyCreate, CompanyUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any

class CompanyController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('companies', conn)

    def create(self, company_data: CompanyCreate) -> int:
        data = company_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['user_id'],
                    data['company_name'],
                    data['business_type'],
                    data['address'],
                    data['contact_person'],
                    data['logo'],
                    data['description'],
                    data['company_status'].value, 
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
        
    def update(self, id: int, company_data: CompanyUpdate) -> bool:
        data = company_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data['company_name'],
                    data['business_type'],
                    data['address'],
                    data['contact_person'],
                    data['logo'],
                    data['description'],
                    data['rating'],
                    data['total_jobs_posted'],
                    data['balance'],
                    data['status'].value if data['status'] else None
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False
    
    def get_company_with_user(self, company_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT c.*, u.email, u.phone, u.user_type 
            FROM companies c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """
        with self.conn.get_cursor() as cursor:
            cursor.execute(query, (company_id,))
            return cursor.fetchone()