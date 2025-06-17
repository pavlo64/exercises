from pydantic import BaseModel

class Category(BaseModel):
    name: str
    id: int
class Brand(BaseModel):
    brand_id: int
    name: str
    rate: int | None
    category : int | None
