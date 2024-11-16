import logging
from io import BytesIO

from fastapi import APIRouter, Form, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from app.services.ics_generator import create_ics
from app.services.parser import parse_event_details, construct_prompt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/process")
async def process_event(event_text: str = Form(...)):
    """
    Process the event text input, create an ICS file, and return it to the user.

    Args:
        event_text (str): The raw event details provided by the user.

    Returns:
        StreamingResponse: The generated ICS file for download.
    """
    try:
        # Construct a detailed prompt
        prompt = construct_prompt(event_text)

        # Parse event details using the prompt
        event_details = parse_event_details(prompt)
        if not event_details:
            raise HTTPException(status_code=400, detail="Failed to parse event details.")

        # Create ICS content
        ics_file_path = create_ics(event_details)

        # Read the ICS file content
        with open(ics_file_path, "rb") as f:
            ics_content = f.read()

        # Return the ICS file as a downloadable response
        return StreamingResponse(
            BytesIO(ics_content),
            media_type="text/calendar",
            headers={"Content-Disposition": 'attachment; filename="event.ics"'},
        )

    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
