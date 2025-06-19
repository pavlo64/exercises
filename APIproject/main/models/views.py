from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str
    rate: int | None = None
    category: int | None = None

class BrandUpdate(BaseModel):
    name: str | None = None
    rate: int | None = None
    category: int | None = None

class CategoryUpdate(BaseModel):
    name: str