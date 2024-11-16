import json
import logging
from typing import Optional

import ollama  # Assuming you are using Ollama for language model processing

from app.models.ics_model import ICSAttributes


def construct_prompt(event_text: str) -> str:
    """
    Constructs a prompt to guide the language model to parse event details.

    Args:
        event_text (str): The raw event description provided by the user.

    Returns:
        str: The constructed prompt.
    """
    return f"""
Extract the event details from the following text and return them as a JSON object that conforms to the schema below.
Omit any fields where the value is empty or unavailable.

Input: "{event_text}"

Schema:
{{
    "uid": "string (required): A unique identifier for the event.",
    "dtstart": "string (required): The event start date and time in ISO 8601 format (e.g., '2023-11-20T10:00:00').",
    "dtend": "string (optional): The event end date and time in ISO 8601 format (e.g., '2023-11-20T11:00:00').",
    "summary": "string (required): A brief title or summary of the event.",
    "description": "string (optional): A detailed description of the event.",
    "location": "string (optional): The physical or virtual location of the event.",
    "categories": "list of strings (optional): Tags or categories for the event.",
    "status": "string (optional): The event's status (e.g., 'CONFIRMED', 'TENTATIVE', 'CANCELLED').",
    "priority": "integer (optional): The priority level of the event (0-9).",
    "event_class": "string (optional): The classification of the event (e.g., 'PUBLIC', 'PRIVATE', 'CONFIDENTIAL').",
    "organizer": {{
        "name": "string (optional): The name of the event organizer.",
        "email": "string (required if organizer is provided): The email address of the organizer."
    }},
    "attendees": [
        {{
            "name": "string (optional): The name of the attendee.",
            "email": "string (required): The email address of the attendee."
        }}
    ],
    "url": "string (optional): A URL related to the event.",
    "rrule": "string (optional): A recurrence rule in string format (e.g., 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO')."
}}

Ensure the JSON is well-formed, and do not include any fields with empty or null values.
"""


def parse_event_details(event_text: str) -> Optional[ICSAttributes]:
    """
    Parses the user-provided text into an ICSAttributes object.

    Args:
        event_text (str): Raw user input describing the event.

    Returns:
        Optional[ICSAttributes]: Parsed and validated ICSAttributes object.
    """
    try:
        # Construct a prompt for the language model
        prompt = construct_prompt(event_text)

        # Send the prompt to the language model
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )

        # Log the raw response for debugging
        logging.debug(f"Raw API response: {response}")

        # Extract the content from the response
        message_content = response.get('message', {}).get('content', '')

        if not message_content:
            logging.error("Language model returned an empty response.")
            return None

        # Ensure the response content is JSON
        try:
            parsed_data = json.loads(message_content)
        except json.JSONDecodeError:
            logging.error("Response content is not valid JSON.")
            logging.error(f"Raw message content: {message_content}")
            return None

        # Clean the URL field if empty
        if parsed_data.get("url") == "":
            parsed_data["url"] = None

        # Validate and return the ICSAttributes object
        return ICSAttributes(**parsed_data)

    except Exception as e:
        logging.error(f"Error occurred while parsing event details: {e}")
        return None
