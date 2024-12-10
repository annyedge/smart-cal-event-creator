from pydantic import BaseModel


class EventRequest(BaseModel):
    event_text: str
