from typing import TypeVar, Generic, Optional, List, Dict, Any
from database.connection import Connection
from abc import ABC, abstractmethod
import psycopg2

T = TypeVar('T') # Type variable for generic type

class BaseController(Generic[T], ABC):
    def __init__(self, table_name: str, conn: Connection):
        self.table_name = table_name
        self.conn = conn

    @property
    def cursor(self):
        return self.conn.cursor
    
    def get_by_id(self, id: int) -> Optional[Dict[str, any]]:
        try:
            query = f"SELECT * FROM {self.table_name} WHERE id = %s"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching record by ID: {e}")
            return None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Dict[str, any]]:
        try:
            query = f"SELECT * FROM {self.table_name} LIMIT %s OFFSET %s"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (limit, offset))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching all records: {e}")
            return []
    
    def count(self) -> int:
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else 0
        except psycopg2.Error as e:
            print(f"Error counting records: {e}")
            return 0

    #Basic CRUD operations
    @abstractmethod
    def create(self, data) -> bool:
        pass
    
    @abstractmethod    
    def update(self, id: int, data) -> bool:
        pass

    def delete(self, id: int) -> bool:
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
                return cursor.rowcount > 0
        except psycopg2.Error as e:
            print(f"Error deleting record in table {self.table_name}: {e}")
            return False