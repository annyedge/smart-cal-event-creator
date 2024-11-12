import ollama
from app.models.event_model import EventDetails

def parse_event_details(text: str) -> EventDetails:
    # Implement actual Ollama parsing logic
    parsed_data = ollama.parse_event(text)
    # Map parsed data to EventDetails model
    event_details = EventDetails(**parsed_data)
    return event_details
