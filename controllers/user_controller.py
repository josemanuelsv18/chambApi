from schemas.user import UserCreate, UserUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
import psycopg2
from passlib.context import CryptContext

class UserController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('users', conn)
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            argon2__time_cost=3, # Iteration count
            argon2__memory_cost=65536, # 64 MB
            argon2__parallelism=4, # Number of threads
            argon2__hash_len=32, # Length of the hash
            argon2__salt_len=16 # Length of the salt
        )


    def create(self, user_data: UserCreate) -> bool:
        data = user_data.model_dump()
        hashed_password = self.pwd_context.hash(data['password'])
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s)",
                    (
                        data['email'],
                        hashed_password,
                        data['phone'],
                        data['user_type'].value if data['user_type'] else None,
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"user creat, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False
        
    def update(self, id: int, user_data: UserUpdate) -> bool:
        data = user_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s, %s, %s, %s, %s)",
                    (
                        id,
                        data.get('email'),
                        data.get('password'),
                        data.get('phone'),
                        data['user_type'].value if data.get('user_type') else None,
                        data.get('is_active'),
                        data.get('is_verified')  
                    )
                )
                return True
        except psycopg2.Error as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def exists_by_email(self, email: str) -> bool:
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(f"SELECT check_email_exists_{self.table_name}(%s)", (email,))
                return True
        except psycopg2.Error as e:
            print(f"Error checking existence by email: {e}")
            return False

    def exists_by_phone(self, phone: str) -> bool:
        try:  
            with self.conn.get_cursor() as cursor:
                cursor.execute(f"SELECT check_phone_exists_{self.table_name}(%s)", (phone,))
                return True
        except psycopg2.Error as e:
            print(f"Error checking existence by phone: {e}")
            return False