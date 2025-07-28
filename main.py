from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Connection
from routes.user_routes import get_user_routes
from routes.worker_routes import get_worker_routes
from routes.admin_routes import get_admin_routes
from routes.company_routes import get_company_routes
from routes.job_offer_routes import get_job_offer_routes
from routes.application_routes import get_application_routes
from routes.job_routes import get_job_routes
from routes.payment_routes import get_payment_routes
from routes.review_routes import get_review_routes
#from routes.auth_routes import get_auth_routes

class MainApp:
    def __init__(self):
        self.app = FastAPI() 
        self.setup_cors()  # Agregar CORS antes de las rutas
        self.conn = Connection()
        self.include_routes()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Permite todas las origins
            allow_credentials=True,
            allow_methods=["*"],  # Permite todos los métodos (GET, POST, OPTIONS, etc.)
            allow_headers=["*"],  # Permite todos los headers
        )

    def include_routes(self):
       #self.app.include_router(get_auth_routes(self.conn))  # Agregar auth routes primero
        self.app.include_router(get_user_routes(self.conn))
        self.app.include_router(get_worker_routes(self.conn))
        self.app.include_router(get_admin_routes(self.conn))
        self.app.include_router(get_company_routes(self.conn))
        self.app.include_router(get_job_offer_routes(self.conn))
        self.app.include_router(get_application_routes(self.conn))
        self.app.include_router(get_job_routes(self.conn))
        self.app.include_router(get_payment_routes(self.conn))
        self.app.include_router(get_review_routes(self.conn))

main_app = MainApp()
app = main_app.app