from sqlalchemy import Column, Integer, BigInteger, String
from app.db.base import Base

class UserSettingsModel(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)

    digest_country = Column(String, default="us")
    digest_page = Column(Integer, default=1)

    search_country = Column(String, default="us")
    search_page = Column(Integer, default=1)
    sort_by = Column(String, default="publishedAt")    
    time_for_search = Column(Integer, default=30)
