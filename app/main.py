from io import BytesIO

from fastapi import FastAPI, Form, Request
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.ics_generator import create_ics
from app.services.parser import parse_event_details

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process")
async def process_event(event_text: str = Form(...)):
    try:
        event_details = parse_event_details(event_text)
        ics_content = create_ics(event_details)
        # Handle payment before proceeding
        # process_payment()
        return StreamingResponse(
            BytesIO(ics_content),
            media_type="text/calendar",
            headers={
                "Content-Disposition": 'attachment; filename="event.ics"'
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
