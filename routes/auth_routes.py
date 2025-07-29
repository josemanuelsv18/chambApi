from fastapi import APIRouter, HTTPException, status, Depends
from controllers.auth_controller import AuthController
from schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserTokenData
from dependencies.auth_deps import get_current_active_user, get_auth_controller

def get_auth_routes(conn) -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["authentication"])
    
    @router.post("/login", response_model=TokenResponse)
    async def login(
        login_data: LoginRequest,
        auth_controller: AuthController = Depends(get_auth_controller)
    ):
        """Iniciar sesión"""
        result = auth_controller.login(login_data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        return result

    @router.post("/refresh", response_model=TokenResponse)
    async def refresh_token(
        refresh_data: RefreshTokenRequest,
        auth_controller: AuthController = Depends(get_auth_controller)
    ):
        """Renovar access token"""
        result = auth_controller.refresh_access_token(refresh_data.refresh_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado"
            )
        return result

    @router.get("/me", response_model=UserTokenData)
    async def get_current_user_info(
        current_user: UserTokenData = Depends(get_current_active_user)
    ):
        """Obtener información del usuario actual"""
        return current_user

    @router.post("/logout")
    async def logout():
        """Cerrar sesión (el frontend debe eliminar los tokens)"""
        return {"message": "Sesión cerrada exitosamente"}

    return router