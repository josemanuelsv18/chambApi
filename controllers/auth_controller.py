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
            schemes=["argon2"],
            argon2__time_cost=3,
            argon2__memory_cost=65536,
            argon2__parallelism=4,
            argon2__hash_len=32,
            argon2__salt_len=16
        )

    @property
    def cursor(self):
        return self.conn.cursor

    def authenticate_user(self, login_data: LoginRequest) -> Optional[UserTokenData]:
        # Authenticate user by checking email and password
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, email, password, user_type, is_active, is_verified
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
        # Proceso de login completo
        # Autenticar usuario
        user = self.authenticate_user(login_data)  # Era: login_data.email, login_data.password
        if not user:
            return None
        
        # Crear tokens
        token_data = {"sub": str(user.user_id), "email": user.email, "user_type": user.user_type}
        access_token = JWTConfig.create_access_token(token_data)
        refresh_token = JWTConfig.create_refresh_token({"sub": str(user.user_id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        # Renovar access token usando refresh token
        payload = JWTConfig.verify_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return None
        
        user_id = int(payload.get("sub"))
        user = self.get_user_by_id(user_id)
        
        if not user:
            return None
        
        # Crear nuevo access token
        token_data = {"sub": str(user.user_id), "email": user.email, "user_type": user.user_type}
        access_token = JWTConfig.create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,  # Mantener el mismo refresh token
            expires_in=JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )