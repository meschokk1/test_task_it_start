from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class STaskAdd(BaseModel):
    device_id: int
    x: float
    y: float
    z: float

class STask(STaskAdd):
    id: int
    timestamp: datetime

class STaskId(BaseModel):
    ok: bool = True
    task_id: int

class STaskDates(BaseModel):
    start_date: Optional[datetime]=None
    end_date: Optional[datetime]=None