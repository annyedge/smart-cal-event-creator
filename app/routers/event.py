import logging
from datetime import datetime
from io import BytesIO

from fastapi import HTTPException, APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse

from app.models import EventRequest
from app.services.parser import build_ical_from_description  # Adjust path as needed

router = APIRouter()


@router.post("/process", tags=["Events"], response_class=HTMLResponse)
async def create_event(payload: EventRequest):
    event_text = payload.event_text
    """
    Create a calendar event (.ics) from the submitted form text.

    Args:
        event_text (str): The raw event details provided in the form.

    Returns:
        StreamingResponse: The generated .ics file for download.
    """
    try:
        current_time = datetime.now()
        output_file_path = "event.ics"  # or a temporary path you manage

        # Call the parser service to build the ICS file
        build_ical_from_description(event_text, current_time, output_file_path)

        # Read the generated ICS file and return as a response
        with open(output_file_path, "rb") as f:
            ics_content = f.read()

        return StreamingResponse(
            BytesIO(ics_content),
            media_type="text/calendar",
            headers={"Content-Disposition": 'attachment; filename="event.ics"'},
        )
    except Exception as e:
        logging.error(f"Error creating event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
