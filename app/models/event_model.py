from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict


class EventDetails(BaseModel):
    summary: str
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    rrule: Optional[Dict]
    timezone: Optional[str]
