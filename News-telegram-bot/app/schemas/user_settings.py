from pydantic import BaseModel
from typing import Optional

class UserSettings(BaseModel):
    user_id: int

    digest_country: Optional[str] = "us"
    digest_page: Optional[int] = 1

    search_country: Optional[str] = "us"
    search_page: Optional[int] = 5
    sort_by: Optional[str] = "publishedAt"
    time_for_search: Optional[int] = 1
