from datetime import datetime
from pydantic import BaseModel


class ApiRequestsSchema(BaseModel):
    request_type: str
    path: str
    response: str
    status_code: int
    created_at: datetime