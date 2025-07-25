from fastapi import APIRouter, Depends, HTTPException, status
from typing import Generic, TypeVar, List, Optional
from ..controllers.base_controller import BaseController

T = TypeVar('T')
CreateSchema = TypeVar('CreateSchema')
UpdateSchema = TypeVar('UpdateSchema')

class BaseRoutes(Generic[T, CreateSchema, UpdateSchema]):
    def __init__(self, controller: BaseController, prefix: str, tags: Optional[list] = None):
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self.controller = controller
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=List[T])
        def get_all():
            items = self.controller.get_all()
            if not items:
                raise HTTPException(status_code=404, detail="No items found")
            return items
        
        @self.router.get("/{item_id}", response_model=Optional[T])
        def get_by_id(item_id: int):
            item = self.controller.get_by_id(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item
        
        @self.router.post("/", response_model=int)
        def create(item: CreateSchema):
            item_id = self.controller.create(item)
            if not item_id:
                raise HTTPException(status_code=400, detail="Failed to create item")
            return item_id
        
        @self.router.put("/{item_id}", response_model=bool)
        def update(item_id: int, item: UpdateSchema):
            success = self.controller.update(item_id, item)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to update item")
            return success

        @self.router.delete("/{item_id}", response_model=bool)
        def delete(item_id: int):
            success = self.controller.delete(item_id)
            if not success:
                raise HTTPException(status_code=400, detail="Failed to delete item")
            return success