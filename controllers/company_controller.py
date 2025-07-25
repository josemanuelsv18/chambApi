from schemas.company import CompanyCreate, CompanyUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any

class CompanyController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('companies', conn)

    def create(self, company_data: CompanyCreate) -> bool:
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
                    data['company_status'].value if data['company_status'] else None,
                    0
                ]
                cursor.callproc(f'sp_create_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False
        
    def update(self, id: int, company_data: CompanyUpdate) -> bool:
        data = company_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('company_name'),
                    data.get('business_type'),
                    data.get('address'),
                    data.get('contact_person'),
                    data.get('logo'),
                    data.get('description'),
                    data.get('rating'),
                    data.get('total_jobs_posted'),
                    data.get('balance'),
                    data['status'].value if data.get('status') else None
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False
    
    def get_company_with_user(self, company_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT c.*, u.email, u.phone, u.user_type 
                FROM companies c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (company_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching company with user: {e}")
            return None
        
    def get_company_by_name(self, company_name: str) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM companies 
                WHERE company_name = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (company_name,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching company by name: {e}")
            return None
        
    def get_company_by_type(self, business_type: str) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM companies 
                WHERE business_type = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (business_type,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching company by type: {e}")
            return []