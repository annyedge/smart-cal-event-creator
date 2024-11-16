import logging
from io import BytesIO

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import StreamingResponse

from app.services.ics_generator import create_ics
from app.services.parser import parse_event_details

router = APIRouter()


@router.post("/create")
async def create_event(event_text: str = Form(...)):
    """
    Create a calendar event (.ics) from a user-provided text description.

    Args:
        event_text (str): The raw event details provided by the user.

    Returns:
        StreamingResponse: The generated .ics file for download.
    """
    try:
        # Parse event details from text
        parsed_event = parse_event_details(event_text)
        if not parsed_event:
            raise HTTPException(status_code=400, detail="Failed to parse event details.")

        # Generate the .ics file
        ics_file_path = create_ics(parsed_event)

        # Stream the .ics file to the user
        with open(ics_file_path, "rb") as f:
            ics_content = f.read()

        return StreamingResponse(
            BytesIO(ics_content),
            media_type="text/calendar",
            headers={"Content-Disposition": 'attachment; filename="event.ics"'},
        )
    except Exception as e:
        logging.error(f"Error creating event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
