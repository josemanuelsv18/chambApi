from database.connection import Connection
from schemas.auth import LoginRequest, TokenResponse, UserTokenData
from config.jwt_config import JWTConfig
from passlib.context import CryptContext
from typing import Optional
import psycopg2

class AuthController:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.pwd_context = CryptContext(
            schemes=["aragon2"],
            argon2__time_cost=3,  # Iteration count
            argon2__memory_cost=65536,  # 64 MB
            argon2__parallelism=4,  # Number of threads
            argon2__hash_len=32,  # Length of the hash
            argon2__salt_len=16  # Length of the salt
        )

    @property
    def cursor(self):
        return self.conn.cursor

    def authenticate_user(self, login_data: LoginRequest) -> Optional[UserTokenData]:
        # Authenticate user by checking email and password
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, email, password, usert_type, is_active, is_verified
                    FROM users
                    WHERE email = %s AND is_active = true
                """, (login_data.email.lower(),))

                user = cursor.fetchone()

                if not user:
                    return None
                
                # verify password
                if not self.pwd_context.verify(login_data.password, user['password']):
                    return None
                
                return UserTokenData(
                    user_id=user['id'],
                    email=user['email'],
                    user_type=user['user_type'],
                    is_active=user['is_active'],
                    is_verified=user['is_verified']
                )
        
        except psycopg2.Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, id: int):
        # fetch user by ID for token validation
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, email, user_type, is_active, is_verified 
                    FROM users 
                    WHERE id = %s AND is_active = true
                """, (id,))

                user = cursor.fetchone()
                if not user:
                    return None
                
                return UserTokenData(
                    user_id=user['id'],
                    email=user['email'],
                    user_type=user['user_type'],
                    is_active=user['is_active'],
                    is_verified=user['is_verified']
                )
        except psycopg2.Error as e:
            print(f"Error fetching user by ID: {e}")
            return None
        
    def login(self, login_data: LoginRequest) -> Optional[TokenResponse]:
        user = self.authenticate_user(login_data.email, login_data.password)
        if not user:
            return None
        
    def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        pass