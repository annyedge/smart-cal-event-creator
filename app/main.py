import logging
from io import BytesIO

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.ics_generator import create_ics
from app.services.parser import parse_event_details

app = FastAPI(
    title="Event2Calendar",
    description="Convert event details into .ics calendar files.",
    version="1.0.0",
)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=HTMLResponse)
async def create_event(event_text: str = Form(...)):
    """
    Create a calendar event (.ics) from the submitted form text.
    """
    try:
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
