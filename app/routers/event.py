# event.py

from datetime import datetime

from fastapi import HTTPException, APIRouter
from starlette.responses import FileResponse

from app.models.input import EventDescription
from app.services.parser import build_ical_from_description  # Adjust path as needed

router = APIRouter()


@router.post("/process", tags=["Events"])
async def process_event(event_desc: EventDescription):
    current_timestamp = datetime.now()
    event_description = event_desc.description
    output_file_path = "event.ics"
    try:
        ics_file_path = build_ical_from_description(event_description, current_timestamp, output_file_path)
        return FileResponse(ics_file_path, media_type="text/calendar")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
