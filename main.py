from fastapi import FastAPI
from .database.connection import Connection
from .routes.user_routes import UserRoutes

app = FastAPI()
conn = Connection()

# Incluye las rutas de usuario
user_routes = UserRoutes.get_user_routes(conn)
app.include_router(user_routes)