from icalendar import Calendar, Event
from app.models.event_model import EventDetails

def create_ics(event_details: EventDetails) -> bytes:
    cal = Calendar()
    event = Event()
    event.add('summary', event_details.summary)
    event.add('dtstart', event_details.start_time)
    event.add('dtend', event_details.end_time)
    event.add('location', event_details.location)
    if event_details.rrule:
        event.add('rrule', event_details.rrule)
    cal.add_component(event)
    return cal.to_ical()

from datetime import datetime
import pytz

def get_timezone_aware_datetime(dt_str, timezone_str):
    tz = pytz.timezone(timezone_str)
    naive_datetime = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    aware_datetime = tz.localize(naive_datetime)
    return aware_datetime

def add_recurrence(event, recurrence_details):
    event.add('rrule', recurrence_details)

