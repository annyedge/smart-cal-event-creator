import json
import logging
from typing import Optional

import ollama

from app.models.ics_model import ICSAttributes

# Configure logging
logging.basicConfig(level=logging.INFO)


def construct_prompt(event_text: str) -> str:
    """
    Constructs a prompt for the llama model to extract event details from user input.

    Args:
        event_text (str): Free-form text input provided by the user.

    Returns:
        str: The constructed prompt.
    """
    return f"""
Extract the following event details from the user-provided text and return them as a JSON object.

Input Text: "{event_text}"

The JSON object should follow this schema:
{{
    "uid": "Unique identifier for the event (string, required).",
    "dtstart": "Start date and time of the event in ISO 8601 format (string, required, e.g., '2023-11-20T10:00:00').",
    "dtend": "End date and time of the event in ISO 8601 format (string, optional, e.g., '2023-11-20T11:00:00').",
    "summary": "A brief title or summary of the event (string, required).",
    "description": "Detailed description of the event (string, optional).",
    "location": "The physical or virtual location of the event (string, optional).",
    "categories": "A list of categories or tags for the event (list of strings, optional).",
    "status": "The status of the event (string, optional, e.g., 'CONFIRMED', 'TENTATIVE', 'CANCELLED').",
    "priority": "Priority level of the event (integer, optional, 0-9).",
    "event_class": "Classification of the event (string, optional, e.g., 'PUBLIC', 'PRIVATE', 'CONFIDENTIAL').",
    "organizer": {{
        "name": "Name of the event organizer (string, optional).",
        "email": "Email address of the organizer (string, optional, valid email format)."
    }},
    "attendees": [
        {{
            "name": "Name of the attendee (string, optional).",
            "email": "Email address of the attendee (string, required, valid email format)."
        }}
    ],
    "rrule": "Recurrence rule for repeating events (string, optional, e.g., 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO')."
}}

If any information is missing or cannot be inferred from the text, leave it out of the JSON object. Ensure the JSON is valid and compatible with the schema above.
"""


def parse_event_details(prompt: str) -> Optional[ICSAttributes]:
    """
    Parses event details from a prompt string using the Ollama API and returns an ICSAttributes object.

    Args:
        prompt (str): The input prompt containing event details.

    Returns:
        Optional[ICSAttributes]: The parsed ICSAttributes object or None if parsing fails.
    """
    try:
        # Send a message to the Ollama API
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )

        # Extract the content from the response
        message_content = response.get('message', {}).get('content', '')

        if not message_content:
            logging.error("Ollama API returned an empty response.")
            return None

        # Parse the response content into a dictionary
        try:
            parsed_data = json.loads(message_content)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse response content as JSON: {e}")
            return None

        # Validate and return the ICSAttributes object
        event_details = ICSAttributes(**parsed_data)
        logging.info("Successfully parsed event details into ICSAttributes.")
        return event_details

    except Exception as e:
        logging.error(f"An error occurred while parsing event details: {e}")
        return None
