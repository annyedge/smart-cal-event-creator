from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.event import router as event_router

# Create FastAPI app instance
app = FastAPI(
    title="Smart Calendar Event Creator",
    description="A service to generate .ics calendar events",
    version="1.0.0",
)

# Include the event router
app.include_router(event_router, prefix="/api/events", tags=["Events"])

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static"
)


# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Smart Calendar Event Creator!"}
