from pydantic import BaseModel


class Brand(BaseModel):
    brand_id: int
    name: str
    rate: int | None
    catalogue : str | None
