from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ItemIn(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# tiny in-memory store for demo
DB: dict[int, dict] = {}
NEXT_ID = 1

@router.post("/", status_code=201)
def create_item(item: ItemIn):
    global NEXT_ID
    item_id = NEXT_ID
    NEXT_ID += 1
    DB[item_id] = {"id": item_id, **item.model_dump()}
    print(f"Item created with ID {item_id}")
    return DB[item_id]

@router.get("/{item_id}",  status_code=200)
def get_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=418, detail=f"Item {item_id} not found in DB")
    return DB[item_id]

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    del DB[item_id]     