
from pydantic import BaseModel
from datetime import datetime

class IncidentCreate(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

class IncidentChangeStatus(BaseModel):
    id: int
    status: str

class IncidentDelete(BaseModel):
    id: int
