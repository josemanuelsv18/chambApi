import os
import mysql.connector
from dotenv import load_dotenv
from contextlib import contextmanager

class Connection:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        # Inicializar la conexión y el cursor
        self._connection = None
        self._cursor = None

    #propiedades computadas para manejar la conexión y el cursor
    @property
    def connection(self):
        if not self._connection or not self._connection.is_connected(): # Verifica si la conexión está abierta
            self.open_connection()
        return self._connection
    
    @property
    def cursor(self):
        if not self._cursor or not self._connection.is_connected(): # Verifica si el cursor está abierto
            self.open_connection()
            self._cursor = self._connection.cursor()
        return self._cursor

    # Método para abrir la conexión a la base de datos
    def open_connection(self):
        try:
            # Crear una nueva conexión a la base de datos
            self._connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self._connection.is_connected(): # Verifica si la conexión se ha establecido correctamente
                print("Connected to MySQL version: ", self.connection.get_server_info())
                self._cursor = self._connection.cursor(dictionary=True) # Cursor con diccionario para resultados más legibles
                return True
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}")
            return False
        
    def close_connection(self):
        if self._cursor:
            self._cursor.close()
            print("Cursor closed.")
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Connection closed.")

    @contextmanager
    def get_cursor(self):
        try:
            yield self.cursor
            self.connection.commit()  # Commit any changes if needed
        except Exception as e:
            self.connection.rollback()  # Rollback in case of error
            print(f"An error occurred: {e}")
            raise e