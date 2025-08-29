from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    image_url: Optional[str] = None