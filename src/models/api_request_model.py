from sqlalchemy import Column, DateTime, Integer, String
from src.config.database_config import Base

class APIrequestModel(Base):
    __tablename__ = "api_requests"

    id = Column(Integer, primary_key=True)
    request_type = Column(String, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    response = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    