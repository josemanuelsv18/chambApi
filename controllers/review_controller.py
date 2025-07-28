from schemas.review import ReviewCreate, ReviewUpdate
from database.connection import Connection
from controllers.base_controller import BaseController
from typing import Optional, Dict, Any
from enums.enums import ReviewerType
import psycopg2

class ReviewController(BaseController):
    def __init__(self, conn: Connection):
        super().__init__('reviews', conn)

    def create(self, review_data: ReviewCreate) -> bool:
        data = review_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_create_{self.table_name}(%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        data['job_id'],
                        data['reviewer_id'],
                        data['reviewee_id'],
                        data['reviewer_type'].value if data.get('reviewer_type') else None,
                        data['reviewee_type'].value if data.get('reviewee_type') else None,
                        data['rating'],
                        data.get('comment'),
                        0
                    )
                )
                result = cursor.fetchone()
                print(f"Review created, id: {result}")
                return True
        except psycopg2.Error as e:
            print(f"Error creating record in table {self.table_name}: {e}")
            return False

    def update(self, id: int, review_data: ReviewUpdate) -> bool:
        data = review_data.model_dump()
        try:
            with self.conn.get_cursor() as cursor:
                cursor.execute(
                    f"SELECT sp_update_{self.table_name}(%s, %s, %s)",
                    (
                        id,
                        data.get('rating'),
                        data.get('comment')
                    )
                )
                return True
        except psycopg2.Error as e:
            print(f"Error updating record in table {self.table_name}: {e}")
            return False

    def get_reviews_by_job(self, job_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM reviews
                WHERE job_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (job_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching reviews by job: {e}")
            return []

    def get_reviews_by_reviewer(self, reviewer_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM reviews
                WHERE reviewer_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (reviewer_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching reviews by reviewer: {e}")
            return []

    def get_reviews_by_reviewee(self, reviewee_id: int) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM reviews
                WHERE reviewee_id = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (reviewee_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching reviews by reviewee: {e}")
            return []

    def get_reviews_by_type(self, reviewer_type: ReviewerType) -> list[Dict[str, Any]]:
        try:
            query = """
                SELECT * FROM reviews
                WHERE reviewer_type = %s
            """
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (reviewer_type.value,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching reviews by type: {e}")
            return []