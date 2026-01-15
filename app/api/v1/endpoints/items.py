"""
app/api/v1/endpoints/items.py

Item CRUD operations.
Demonstrates:
- Protected routes (Depends(deps.get_current_active_user))
- Path parameters ({id})
- Response models
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

from app.api import deps
from app.schemas import item as item_schema
from app.schemas import user as user_schema
from app.db.session import db

router = APIRouter()

@router.get("/", response_model=List[item_schema.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    # Filter items owned by the current user (or maybe all items? Let's show all for simplicity, or just user's)
    # Let's filter by user for realism
    user_items = [item for item in db.items.values() if item["owner_id"] == current_user.id]
    return user_items[skip : skip + limit]

@router.post("/", response_model=item_schema.Item)
def create_item(
    *,
    item_in: item_schema.ItemCreate,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item_data = item_in.model_dump() # Pydantic v2
    item_id = db.item_id_counter
    db.item_id_counter += 1
    
    new_item = {
        "id": item_id,
        "title": item_data["title"],
        "description": item_data.get("description"),
        "owner_id": current_user.id
    }
    db.items[item_id] = new_item
    return new_item

@router.put("/{id}", response_model=item_schema.Item)
def update_item(
    *,
    id: int,
    item_in: item_schema.ItemUpdate,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = db.items.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item["owner_id"] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    update_data = item_in.model_dump(exclude_unset=True)
    
    # Update dict
    for field in update_data:
        item[field] = update_data[field]
        
    db.items[id] = item
    return item

@router.get("/{id}", response_model=item_schema.Item)
def read_item(
    *,
    id: int,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = db.items.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item["owner_id"] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item

@router.delete("/{id}", response_model=item_schema.Item)
def delete_item(
    *,
    id: int,
    current_user: user_schema.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = db.items.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item["owner_id"] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    del db.items[id]
    return item
