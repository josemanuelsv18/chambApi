from schemas.worker import WorkerCreate, WorkerUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
import psycopg2

class WorkerController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('workers', conn)

    def create(self, worker_data: WorkerCreate) -> bool:
        data = worker_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        data['user_id'],
                        data['first_name'],
                        data['last_name'],
                        data['date_of_birth'],
                        data.get('profile_picture'),
                        data.get('bio'),
                        data['experience_level'].value if data['experience_level'] else None,
                        data['location'],
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"Worker created, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False
        
    def update(self, id: int, worker_data: WorkerUpdate) -> bool:
        data = worker_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
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
                    )
                )
                return True
        except psycopg2.Error as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False
        
    def get_worker_with_user(self, worker_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = """
                SELECT w.*, u.email, u.phone, u.user_type 
                FROM workers w
                JOIN users u ON w.user_id = u.id
                WHERE w.id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (worker_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching worker with user: {e}")
            return None