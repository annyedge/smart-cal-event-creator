# prompts.py

# Format prompts for the LLM
format_instructions = """
Provide a JSON object with the following fields:

- uid (string): A unique identifier for the event.
- dtstart (string): The event start date and time in ISO 8601 format.
- dtend (string, optional): The event end date and time in ISO 8601 format.
- summary (string): A brief title or summary of the event.
- description (string, optional): A detailed description of the event.
- location (string, optional): The physical or virtual location of the event.
- categories (list of strings, optional): Tags or categories for the event.
- status (string, optional): The event's status (e.g., 'CONFIRMED', 'TENTATIVE', 'CANCELLED').
- priority (integer, optional): The priority level of the event (0-9).
- event_class (string, optional): The classification of the event (e.g., 'PUBLIC', 'PRIVATE', 'CONFIDENTIAL').
- organizer (object, optional): The organizer of the event, with fields:
  - name (string, optional): The name of the organizer.
  - email (string): The email address of the organizer.
- attendees (list of objects, optional): A list of attendees, each with fields:
  - name (string, optional): The name of the attendee.
  - email (string): The email address of the attendee.
- url (string, optional): A URL related to the event.
- rrule (string, optional): A recurrence rule in string format (e.g., 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO').

Ensure the JSON is well-formed and does not include any fields with empty or null values.
Do not include any explanations or additional text. Only output the JSON object.
"""

# Prompt template for parsing event details
prompt_template = """
Your task is to extract event details from the given text and return them as a JSON object matching the specified format.

Instructions:
{format_instructions}

Text:
"{event_text}"

Output:
"""
