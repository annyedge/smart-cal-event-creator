from io import BytesIO

from fastapi import APIRouter, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.ics_generator import create_ics
from app.services.parser import parse_event_details

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/process")
async def process_event(event_text: str = Form(...)):
    event_details = parse_event_details(event_text)
    ics_content = create_ics(event_details)
    # Implement payment processing here
    return StreamingResponse(
        BytesIO(ics_content),
        media_type="text/calendar",
        headers={"Content-Disposition": 'attachment; filename="event.ics"'},
    )
