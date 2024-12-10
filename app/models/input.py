# input.py

from pydantic import BaseModel


class EventDescription(BaseModel):
    description: str
