from ..schemas.worker import WorkerCreate, WorkerUpdate
from ..database.connection import Connection
from .base_controller import BaseController
from typing import Optional, Dict, Any

class WorkerController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('workers', conn)

    def create(self, worker_data: WorkerCreate) -> int:
        data = worker_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    data['user_id'],
                    data['first_name'],
                    data['last_name'],
                    data['date_of_birth'],
                    data.get('profile_picture'),
                    data.get('bio'),
                    data['experience_level'].value if data['experience_level'] else None,
                    data['location'],
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
        
    def update(self, id: int, worker_data: WorkerUpdate) -> bool:
        data = worker_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                args = [
                    id,
                    data.get('first_name'),
                    data.get('last_name'),
                    data.get('date_of_birth'),
                    data.get('profile_picture'),
                    data.get('bio'),
                    data['experience_level'].value if data.get('experience_level') else None,
                    data.get('location'),
                    data.get('rating'),
                    data.get('completed_jobs'),
                    data.get('balance')
                ]
                cursor.callproc(f'sp_update_{self.table_name}', args)
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False
        
    def get_worker_with_user(self, worker_id: int) -> Optional[Dict[str, Any]]:
        # This method retrieves a worker's details along with the associated user information
        query = """
            SELECT w.*, u.email, u.phone, u.user_type 
            FROM workers w
            JOIN users u ON w.user_id = u.id
            WHERE w.id = %s
        """
        with self.conn.get_cursor() as cursor:
            cursor.execute(query, (worker_id,))
            return cursor.fetchone()