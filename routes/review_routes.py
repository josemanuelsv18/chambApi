from fastapi import APIRouter, HTTPException
from controllers.review_controller import ReviewController
from schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate
from routes.base_routes import BaseRoutes
from database.connection import Connection

class ReviewRoutes(BaseRoutes[ReviewResponse, ReviewCreate, ReviewUpdate]):
    def __init__(self, conn: Connection):
        controller = ReviewController(conn)
        super().__init__(controller, prefix="/reviews", tags=["reviews"])

        @self.router.post("/", response_model=bool)
        def create(item: ReviewCreate):
            success = self.controller.create(item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return success
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: ReviewUpdate):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.get("/by_job/{job_id}", response_model=list)
        def get_reviews_by_job(job_id: int):
            reviews = self.controller.get_reviews_by_job(job_id)
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this job")
            return reviews

        @self.router.get("/by_reviewer/{reviewer_id}", response_model=list)
        def get_reviews_by_reviewer(reviewer_id: int):
            reviews = self.controller.get_reviews_by_reviewer(reviewer_id)
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this reviewer")
            return reviews

        @self.router.get("/by_reviewee/{reviewee_id}", response_model=list)
        def get_reviews_by_reviewee(reviewee_id: int):
            reviews = self.controller.get_reviews_by_reviewee(reviewee_id)
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this reviewee")
            return reviews

        @self.router.get("/by_type/{reviewer_type}", response_model=list)
        def get_reviews_by_type(reviewer_type: str):
            reviews = self.controller.get_reviews_by_type(reviewer_type)
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this reviewer type")
            return reviews

def get_review_routes(conn: Connection) -> APIRouter:
    return ReviewRoutes(conn).router