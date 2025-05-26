from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

class Brand(BaseModel):
    id: int
    name: str

class BrandResponse(BaseModel):
    message: str
    brand: Brand

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

@app.post("/brands",  response_model=BrandResponse)
async def create_brand(brand: Brand):
    if brand.id in brand_storage:
        raise HTTPException(status_code=400, detail="Brand ID already exists")
    brand_storage[brand.id] = brand.name
    return {"message": "Brand added", "brand": brand}

@app.put("/brands", response_model=BrandResponse)
async def update_brand(brand: Brand):
    if brand.id  not in brand_storage:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_storage[brand.id] = brand.name
    return {"message": "Brand updated", "brand": brand}

@app.delete("/brands/{brand_id}", response_model=BrandResponse)
async def delete_brand(brand_id: int):
    if brand_id not in brand_storage:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_storage.pop(brand_id)
    return {"message": "Brand deleted", "brand": brand_id}