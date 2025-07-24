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
                    data['email'],
                    data['password'],
                    data['phone'],
                    data['user_type'].value if data['user_type'] else None,
                    data['is_active'],
                    data['is_verified']]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False