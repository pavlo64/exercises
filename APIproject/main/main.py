from fastapi import FastAPI, HTTPException, Query
from typing import List
from .models.models import Brand, Category
from .models.views import BrandUpdate, BrandCreate, CategoryUpdate
from .enums.filters import SortField, SortOrder, RateOperation
import uuid

app = FastAPI()

category_list: List[Category] = [
    Category(id= 1,name="Sport"),
    Category(id= 2,name="Cars"),
]

brand_storage: List[Brand] = [
    Brand(brand_id=1, name="Nike", rate=9, category=1),
    Brand(brand_id=2, name="Adidas", rate=8, category=1),
    Brand(brand_id=3, name="Puma", rate=7, category=1),
    Brand(brand_id=4, name="BMW", rate=6, category=2),
    Brand(brand_id=5, name="AUDI", rate=8, category=2)
]

def get_brand_by_id(brand_id: int) -> Brand | None:
    return next((b for b in brand_storage if b.brand_id == brand_id), None)


def filter_brands(
    name: str | None = None,
    min_rate: int | None = None,
    max_rate: int | None = None) -> List[Brand]:
    result = brand_storage
    if name:
        result = [b for b in result if name.lower() in b.name.lower()]
    if min_rate is not None:
        result = [b for b in result if b.rate >= min_rate]
    if max_rate is not None:
        result = [b for b in result if b.rate <= max_rate]
    return result

def sort_brands(brands: List[Brand], sort_by: SortField, sort_order: SortOrder) -> List[Brand]:
    reverse = sort_order == SortOrder.desc
    return sorted(brands, key=lambda b: getattr(b, sort_by), reverse=reverse)

@app.get("/ping")
def read_root():
    return {"message": "API is working"}

@app.get("/brands", response_model=List[Brand])
async def get_all_brands(
    id: int | None = None,
    name: str | None = None,
    min_rate: int | None = None,
    max_rate: int | None = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    sort_by: SortField | None = None,
    sort_order: SortOrder = SortOrder.asc,
):
    if id is not None:
        brand = get_brand_by_id(id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        return [brand]
    brands = filter_brands(name, min_rate, max_rate)
    if sort_by:
        brands = sort_brands(brands, sort_by, sort_order)
    return brands[offset:offset + limit]

@app.get("/brands/{brand_id}")
async def get_brand(brand_id:int):
    brand = get_brand_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@app.post("/brands")
async def create_brand(brandinput: BrandCreate):
    if any(b.name == brandinput.name for b in brand_storage):
        raise HTTPException(status_code=400, detail="Brand with this name already exists")
    brand = Brand(brand_id = uuid.uuid4().int, name = brandinput.name, rate = brandinput.rate, category=brandinput.category)
    brand_storage.append(brand)
    return brand.brand_id

@app.patch("/brands/{brand_id}")
async def update_brand(brand_id: int, update: BrandUpdate):
    for index, brand in enumerate(brand_storage):
        if brand.brand_id == brand_id:
            updated_brand = brand.model_copy(update={
                "name": update.name if update.name is not None else brand.name,
                "rate": update.rate if update.rate is not None else brand.rate,
                "category": update.category if update.category is not None else brand.categorycatalogue
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

@app.patch("/brands/rate/{brand_id}/{operation}")
async def change_rate(brand_id: int, operation: RateOperation):
    for index, brand in enumerate(brand_storage):
        if brand.brand_id == brand_id:
            current_rate = brand.rate or 0

            if operation == RateOperation.plus:
                new_rate = current_rate + 1
            else:
                new_rate = current_rate - 1

            updated_brand = brand.model_copy(update={
                "name":  brand.name,
                "category": brand.category,
                "rate": new_rate
            })

            brand_storage[index] = updated_brand
            return brand.brand_id

    raise HTTPException(status_code=404, detail="Brand not found")

@app.get("/categories", response_model=List[Brand])
async def get_all_categories():
    return category_list

@app.get("/categories/{id}")
async def get_category(id:int):
    category =  next((b for b in category_list if b.id == id), None)
    if not category:
        raise HTTPException(status_code=404, detail="Brand not found")
    return category

@app.post("/categories")
async def create_category(categoryinput: Category):
    if any(b.name == categoryinput.name for b in category_list):
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    category = Category(id = uuid.uuid4().int, name = categoryinput.name)
    category_list.append(category)
    return category.id

@app.patch("/categories/{id}")
async def update_category(id: int, update: CategoryUpdate):
    for index, category in enumerate(category_list):
        if category.id == id:
            updated_category = category.model_copy(update={
                "name": update.name if update.name is not None else category.name,
            })
            category_list[index] = updated_category
            return category.id

    raise HTTPException(status_code=404, detail="Category not found")

@app.delete("/categories/{id}")
async def delete_category(id: int):
    for index, category in enumerate(category_list):
        if category.id == id:
            category_list.pop(index)
            return category.id
    raise HTTPException(status_code=404, detail="Category not found")
