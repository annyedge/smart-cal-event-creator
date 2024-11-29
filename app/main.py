from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.event import router as event_router

# Create FastAPI app instance
app = FastAPI(
    title="Event2Calendar",
    description="Convert event details into .ics calendar files.",
    version="1.0.0",
)

# Set up templates directory
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the event router
app.include_router(event_router, prefix="/api/events", tags=["Events"])


# Root endpoint to serve the form
@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def read_root(request: Request):
    """
    Render the index.html template as the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})