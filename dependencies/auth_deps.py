from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from controllers.auth_controller import AuthController
from schemas.auth import UserTokenData
from config.jwt_config import JWTConfig
from database.connection import Connection

security = HTTPBearer()

def get_auth_controller() -> AuthController:
    # Dependencia para obtener el controlador de auth
    conn = Connection()
    return AuthController(conn)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_controller: AuthController = Depends(get_auth_controller)
) -> UserTokenData:
    # Dependencia para obtener el usuario actual desde el token
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verificar token
    payload = JWTConfig.verify_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise credentials_exception
    
    # Obtener user_id del token
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception
    
    # Obtener usuario de la base de datos
    user = auth_controller.get_user_by_id(user_id)
    if not user:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: UserTokenData = Depends(get_current_user)
) -> UserTokenData:
    # Dependencia para obtener usuario activo
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

# Dependencias específicas por tipo de usuario
async def require_admin(current_user: UserTokenData = Depends(get_current_active_user)) -> UserTokenData:
    if current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user

async def require_company(current_user: UserTokenData = Depends(get_current_active_user)) -> UserTokenData:
    if current_user.user_type != "company":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo empresas pueden acceder a este recurso"
        )
    return current_user

async def require_worker(current_user: UserTokenData = Depends(get_current_active_user)) -> UserTokenData:
    if current_user.user_type != "worker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo trabajadores pueden acceder a este recurso"
        )
    return current_user