from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

from pydantic.v1 import UUID4

app = FastAPI()

class Brand(BaseModel):
    brand_id: int
    name: str

class BrandResponse(BaseModel):
    message: str
    brand: Brand

class BrandInput(BaseModel):
    name: str

brand_storage: Dict[int, str] = {
    1: "Nike",
    2: "Adidas",
    3: "Puma",
    4: "Reebok",
    5: "New Balance",
    6: "Asics",
    7: "Under Armour"
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/brands", response_model=Dict[int, str])
async def get_all_brands(
    id: Optional[int] = None,
    name: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
                         ):
    if id is not None:
        if id not in brand_storage:
            raise HTTPException(status_code=404, detail="Brand not found")
        return {id: brand_storage[id]}
    filtered = brand_storage
    if name is not None:
        if name not in brand_storage.values():
            raise HTTPException(status_code=404, detail="Brand not found")
        filtered = {k: v for k, v in brand_storage.items() if v == name}
    items = list(filtered.items())
    paginated = items[offset:offset + limit]
    return dict(paginated)

@app.get("/brands/{brand_id}", response_model=Dict[int, str])
async def get_brand(brand_id:int):
    if brand_id not in brand_storage:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {brand_id: brand_storage[brand_id]}

@app.post("/brands")
async def create_brand(brand: BrandInput):
    if brand.name in brand_storage.values():
        raise HTTPException(status_code=400, detail="Brand with this name already exists")
    id = uuid.uuid4().int
    brand_storage[id] = brand.name
    return {id}

@app.patch("/brands/{brand_id}", response_model=BrandResponse)
async def update_brand(brand_id:int, update: BrandInput):
    if brand_id  not in brand_storage:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_storage[brand_id] = update.name
    return {"message": "Brand updated",
            "brand": {
                         "id": brand_id,
                         "name": update.name
                     }
            }

@app.delete("/brands/{brand_id}", response_model=BrandResponse)
async def delete_brand(brand_id: int):
    if brand_id not in brand_storage:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_storage.pop(brand_id)
    return {"message": "Brand deleted", "brand": brand_id}
