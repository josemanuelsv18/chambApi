from typing import TypeVar, Generic, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ..database.connection import Connection
from abc import ABC, abstractmethod

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
        except Exception as e:
            print(f"Error fetching record by ID: {e}")
            return None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Dict[str, any]]:
        try:
            query = f"SELECT * FROM {self.table_name} LIMIT %s OFFSET %s"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (limit, offset))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all records: {e}")
            return None
    
    def count(self) -> int:
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            with self.conn.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error counting records: {e}")
            return 0
    #Basic CRUD operations
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> bool:
        # try:
        #     with self.conn.get_cursor() as cursor:
        #         cursor.callproc(f'sp_create_{self.table_name}', [data['email'], data['password'], data['phone'], data['user_type']])
        #         self.conn.connection.commit()
        #         return True
        # except Exception as e:
        #     print(f"Error creating record in table {self.table_name}: {e}")
        #     return False
        pass
    @abstractmethod    
    def update(self, id:int, data: Dict[str, Any]) -> bool:
        # try:
        #     with self.conn.get_cursor() as cursor:
        #         cursor.callproc(f'sp_update_{self.table_name}', [id, data['email'], data['password'], data['phone'], data['user_type'], data['is_active'], data['is_verified']])
        #         self.conn.connection.commit()
        #         return True
        # except Exception as e:
        #     print(f"Error updating record in table {self.table_name}: {e}")
        #     return False
        pass

    def delete(self, id: int) -> bool:
        # Delete a record from the table
        try:
            with self.conn.get_cursor() as cursor:
                cursor.callproc('DeleteById', [self.table_name, id])
                self.conn.connection.commit()
                return True
        except Exception as e:
            print(f"Error deleting record in table {self.table_name}: {e}")
            return False