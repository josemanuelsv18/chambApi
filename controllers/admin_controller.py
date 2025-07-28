from schemas.admin import AdminCreate, AdminUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
import psycopg2

class AdminController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('administrators', conn)

    def create(self, admin_data: AdminCreate) -> bool:
        data = admin_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s, %s)",
                    (
                        data['user_id'],
                        data['first_name'],
                        data['last_name'],
                        data['admin_level'].value if data['admin_level'] else None,
                        data['created_by_admin_id'],
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"Admin created, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, admin_data: AdminUpdate) -> bool:
        data = admin_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s, %s)",
                    (
                        id,
                        data.get('first_name'),
                        data.get('last_name'),
                        data['admin_level'].value if data.get('admin_level') else None
                    )
                )
                return True
        except psycopg2.Error as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_admin_with_user(self, admin_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT a.*, u.email, u.phone, u.user_type 
                FROM administrators a
                JOIN users u ON a.user_id = u.id
                WHERE a.id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (admin_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching admin with user: {e}")
            return None