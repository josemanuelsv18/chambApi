from ..schemas.user import UserCreate, UserUpdate
from ..database.connection import Connection
from .base_controller import BaseController

class UserController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('users', conn)

    def create(self, user_data: UserCreate) -> int:
        data = user_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['email'],
                    data['password'],
                    data['phone'],
                    data['user_type'].value if data['user_type'] else None,
                    0
                ]
                cursor.callproc(f'sp_create_{self.table_name}', args)
                self.conn.connection.commit()
                for result in cursor.stored_results():
                    new_id = result.fetchone()[0]
                return new_id
        except Exception as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return None
    
    def update(self, id: int, user_data: UserUpdate) -> bool:
        data = user_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('email'),
                    data.get('password'),
                    data.get('phone'),
                    data['user_type'].value if data.get('user_type') else None,
                    data.get('is_active'),
                    data.get('is_verified')
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def exists_by_email(self, email: str) -> bool:
        try:
            query = f"SELECT 1 FROM {self.table_name} WHERE email = %s LIMIT 1"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking existence by email: {e}")
            return False

    def exists_by_phone(self, phone: str) -> bool:
        try:  
            query = f"SELECT 1 FROM {self.table_name} WHERE phone = %s LIMIT 1"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (phone,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking existence by phone: {e}")
            return False