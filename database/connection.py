import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from contextlib import contextmanager

class Connection:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DATABASE")
        # Inicializar la conexión y el cursor
        self._connection = None
        self._cursor = None

    #propiedades computadas para manejar la conexión y el cursor
    @property
    def connection(self):
        if not self._connection or self._connection.closed: # Verifica si la conexión está abierta
            if not self.open_connection():
                return None
        return self._connection
    
    @property
    def cursor(self):
        if not self._cursor or (self._connection and self._connection.closed): # Verifica si el cursor está abierto
            if not self.open_connection():
                return None
            self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self._cursor

    # Método para abrir la conexión a la base de datos
    def open_connection(self):
        try:
            # Crear una nueva conexión a la base de datos con SSL
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                sslmode='require'  # Agregar SSL requerido para Render
            )
            if not self._connection.closed: # Verifica si la conexión se ha establecido correctamente
                # Obtener versión de manera más segura
                try:
                    cursor = self._connection.cursor()
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    print(f"Connected to PostgreSQL: {version}")
                    cursor.close()
                except Exception as e:
                    print(f"Connected to PostgreSQL (version info unavailable): {e}")
                
                self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) # Cursor con diccionario para resultados más legibles
                return True
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            self._connection = None
            self._cursor = None
            return False
        
    def close_connection(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
            print("Cursor closed.")
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None
            print("Connection closed.")

    @contextmanager
    def get_cursor(self):
        # Verificar y abrir conexión si es necesario
        if self._connection is None or self._connection.closed:
            if not self.open_connection():
                raise psycopg2.Error("No se pudo establecer conexión con la base de datos")
        
        # Verificar que tenemos conexión válida antes de continuar
        if self._connection is None:
            raise psycopg2.Error("Conexión a la base de datos no disponible")
            
        try:
            yield self.cursor
            if self._connection and not self._connection.closed:
                self._connection.commit()  # Commit any changes if needed
        except Exception as e:
            # Solo hacer rollback si tenemos conexión válida
            if self._connection and not self._connection.closed:
                self._connection.rollback()  # Rollback in case of error
            print(f"An error occurred: {e}")
            raise e
        finally:
            self.close_connection()