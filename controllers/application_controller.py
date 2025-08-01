from schemas.application import ApplicationCreate, ApplicationUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
import psycopg2

class ApplicationController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('applications', conn)

    def create(self, application_data: ApplicationCreate) -> bool:
        data = application_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO applications (
                        job_offer_id, worker_id, status, applied_at, message
                    ) VALUES (
                        %s, %s, %s, %s, %s
                    ) RETURNING id
                """, (
                    data['job_offer_id'],
                    data['worker_id'],
                    data['application_status'].value,
                    data['applied_at'],
                    data.get('message')
                ))
                result = cursor.fetchone()
                
                # Corregir el acceso al resultado
                if result:
                    # Si result es un diccionario
                    if isinstance(result, dict):
                        print(f"Application created, id: {result.get('id', 'Unknown')}")
                    # Si result es una tupla/lista
                    else:
                        print(f"Application created, id: {result[0]}")
                else:
                    print("Application creation failed - no result returned")
                    return False
                    
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, application_data: ApplicationUpdate) -> bool:
        data = application_data.model_dump(exclude_unset=True)  # Solo campos que se enviaron
        
        if not data:
            return True  # No hay nada que actualizar
        
        try:
            with self.conn.get_cursor() as cursor:
                # Construir la query dinámicamente
                set_clauses = []
                values = []
                
                for key, value in data.items():
                    if key == 'application_status':
                        set_clauses.append("status = %s")
                        values.append(value.value)
                    elif key == 'responded_at':
                        set_clauses.append("responded_at = %s")
                        values.append(value)
                    else:
                        set_clauses.append(f"{key} = %s")
                        values.append(value)
                
                values.append(id)  # Para el WHERE
                
                query = f"""
                    UPDATE applications 
                    SET {', '.join(set_clauses)}, responded_at = NOW()
                    WHERE id = %s
                    RETURNING id
                """
                
                cursor.execute(query, values)
                result = cursor.fetchone()
                
                return bool(result)
                
        except psycopg2.Error as e:
            print(f"Error updating application: {e}")
            return False

    def get_applications_by_worker(self, worker_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM applications
                WHERE worker_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (worker_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching applications by worker: {e}")
            return []

    def get_applications_by_job_offer(self, job_offer_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM applications
                WHERE job_offer_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_offer_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching applications by job offer: {e}")
            return []