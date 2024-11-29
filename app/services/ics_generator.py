from icalendar import Calendar, Event
from app.models.ics_model import ICSAttributes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def create_ics(ics_attributes: ICSAttributes) -> str:
    """
    Create an ICS file from the provided ICSAttributes.

    Args:
        ics_attributes (ICSAttributes): The event details.

    Returns:
        str: The filename of the created ICS file.
    """
    try:
        filename = f"outputs/{ics_attributes.uid}.ics"

        # Create a calendar and an event
        cal = Calendar()
        event = Event()

        # Add mandatory fields
        event.add("summary", ics_attributes.summary)
        event.add("dtstart", ics_attributes.dtstart)
        if ics_attributes.dtend:
            event.add("dtend", ics_attributes.dtend)

        # Add optional fields
        if ics_attributes.location:
            event.add("location", ics_attributes.location)
        if ics_attributes.description:
            event.add("description", ics_attributes.description)
        if ics_attributes.status:
            event.add("status", ics_attributes.status)
        if ics_attributes.rrule:
            event.add("rrule", ics_attributes.rrule)

        # Add attendees
        if ics_attributes.attendees:
            for attendee in ics_attributes.attendees:
                attendee_str = f"MAILTO:{attendee.email}"
                if attendee.name:
                    attendee_str = f"{attendee.name};{attendee_str}"
                event.add("attendee", attendee_str)

        # Add event to calendar
        cal.add_component(event)

        # Write to file
        with open(filename, "wb") as f:
            f.write(cal.to_ical())

        logging.info(f"ICS file '{filename}' created successfully!")
        return filename

    except Exception as e:
        logging.error(f"Failed to create ICS file: {e}")
        raise
