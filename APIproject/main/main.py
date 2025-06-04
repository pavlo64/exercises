from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from .models import Brand
import uuid

app = FastAPI()



class BrandResponse(BaseModel):
    message: str
    brand: Brand

class BrandCreate(BaseModel):
    name: str
    rate: int | None = None
    catalogue: str | None = None

class BrandUpdate(BaseModel):
    name: str | None = None
    rate: int | None = None
    catalogue: str | None = None

brand_storage: List[Brand] = [
    Brand(brand_id=1, name="Nike", rate=9, catalogue="Sportswear"),
    Brand(brand_id=2, name="Adidas", rate=8, catalogue="Sportswear"),
    Brand(brand_id=3, name="Puma", rate=7, catalogue="Sportswear"),
    Brand(brand_id=4, name="BMW", rate=6, catalogue="Cars"),
    Brand(brand_id=5, name="AUDI", rate=8, catalogue="Cars")
]

@app.get("/ping")
def read_root():
    return {"message": "API is working"}

@app.get("/brands", response_model=List[Brand])
async def get_all_brands(
    id: int | None = None,
    name: str | None = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    catalogue: str | None = None,
    min_rate: int | None = None,
    max_rate: int | None = None,
    sort_by: str | None  = Query(None, description="Sort by field: name, rate"),
    sort_order: str = Query("asc", description="asc or desc"),
                         ):
    filtered = brand_storage
    if id is not None:
        brand = next((b for b in brand_storage if b.brand_id == id), None)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        return [brand]
    if name is not None:
        filtered = [b for b in filtered if b.name.lower() == name.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail="Brand not found")
    if catalogue:
        filtered = [b for b in filtered if b.catalogue.lower() == catalogue.lower()]
    if min_rate is not None:
        filtered = [b for b in filtered if b.rate >= min_rate]
    if max_rate is not None:
        filtered = [b for b in filtered if b.rate <= max_rate]
    if sort_by in {"name", "rate"}:
        reverse = sort_order == "desc"
        filtered = sorted(filtered, key=lambda b: getattr(b, sort_by), reverse=reverse)
    paginated = filtered[offset:offset + limit]
    return paginated

@app.get("/brands/{brand_id}")
async def get_brand(brand_id:int):
    if not any(b.brand_id == brand_id for b in brand_storage):
        raise HTTPException(status_code=404, detail="Brand not found")
    return next((b for b in brand_storage if b.brand_id == brand_id), None)

@app.post("/brands")
async def create_brand(brandinput: BrandCreate):
    if any(b.name == brandinput.name for b in brand_storage):
        raise HTTPException(status_code=400, detail="Brand with this name already exists")
    brand = Brand(brand_id = uuid.uuid4().int, name = brandinput.name, rate = brandinput.rate, catalogue=brandinput.catalogue)
    brand_storage.append(brand)
    return brand.brand_id

@app.patch("/brands/{brand_id}")
async def update_brand(brand_id: int, update: BrandUpdate):
    for index, brand in enumerate(brand_storage):
        if brand.brand_id == brand_id:
            updated_brand = brand.model_copy(update={
                "name": update.name if update.name is not None else brand.name,
                "rate": update.rate if update.rate is not None else brand.rate,
                "catalogue": update.catalogue if update.catalogue is not None else brand.catalogue
            })
            brand_storage[index] = updated_brand
            return brand.brand_id

    raise HTTPException(status_code=404, detail="Brand not found")

@app.delete("/brands/{brand_id}")
async def delete_brand(brand_id: int):
    for index, brand in enumerate(brand_storage):
        if brand.brand_id == brand_id:
            brand_storage.pop(index)
            return brand.brand_id

    raise HTTPException(status_code=404, detail="Brand not found")
