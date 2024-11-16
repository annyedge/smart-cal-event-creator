from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime


class Attendee(BaseModel):
    name: Optional[str] = None
    email: EmailStr


class ICSAttributes(BaseModel):
    uid: str
    dtstart: datetime
    dtend: Optional[datetime] = None
    summary: str
    description: Optional[str] = None
    location: Optional[str] = None
    categories: Optional[List[str]] = None
    status: Optional[str] = None  # e.g., TENTATIVE, CONFIRMED, CANCELLED
    priority: Optional[int] = None  # 0-9
    event_class: Optional[str] = None  # e.g., PUBLIC, PRIVATE, CONFIDENTIAL
    organizer: Optional[Attendee] = None
    attendees: Optional[List[Attendee]] = None
    url: Optional[HttpUrl] = None
    recurrence_id: Optional[str] = None
    rrule: Optional[str] = None  # Recurrence rules in string format
    exdate: Optional[List[datetime]] = None  # List of excluded dates
    attach: Optional[List[HttpUrl]] = None  # Attachments


# Example Usage
example_event = ICSAttributes(
    uid="123456789@example.com",
    dtstart=datetime(2023, 11, 16, 12, 0),
    dtend=datetime(2023, 11, 16, 13, 0),
    summary="Team Meeting",
    description="Discuss project updates and milestones.",
    location="Conference Room A",
    categories=["Work", "Meeting"],
    status="CONFIRMED",
    priority=1,
    event_class="PUBLIC",
    organizer=Attendee(name="Jane Smith", email="jane.smith@example.com"),
    attendees=[
        Attendee(name="John Doe", email="john.doe@example.com")
    ],
    url="https://example.com/meetings/123456",
    rrule="FREQ=WEEKLY;INTERVAL=1;BYDAY=MO",
)
