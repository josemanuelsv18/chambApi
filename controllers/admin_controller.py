from ..schemas.admin import AdminCreate, AdminUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any

class AdminController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('administrators', conn)

    def create(self, admin_data: AdminCreate) -> int:
        data = admin_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['user_id'],
                    data['first_name'],
                    data['last_name'],
                    data['admin_level'].value if data['admin_level'] else None,
                    data['created_by_admin_id'],
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

    def update(self, id: int, admin_data: AdminUpdate) -> bool:
        data = admin_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('first_name'),
                    data.get('last_name'),
                    data['admin_level'].value if data.get('admin_level') else None
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_admin_with_user(self, admin_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT a.*, u.email, u.phone, u.user_type 
            FROM admins a
            JOIN users u ON a.user_id = u.id
            WHERE a.id = %s
        """
        with self.conn.get_cursor() as cursor:
            cursor.execute(query, (admin_id,))