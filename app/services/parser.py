import json
from datetime import datetime, timedelta
from dateparser import parse
from icalendar import Calendar, Event
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Assuming prompt_template is defined in your prompts.py file as shown
from app.prompts.prompts import prompt_template

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["current_time", "event_description"]
)


def parse_event_with_langchain(event_description: str, current_timestamp: datetime):
    print("Parsing event with LangChain: ", event_description)

    llm = OllamaLLM(model="llama3.2")
    try:
        sequence = prompt | llm
        result = sequence.invoke(
            input={"current_time": current_timestamp.isoformat(), "event_description": event_description}
        )
        if result is None:
            print("Error: result is None")
            return None
        elif isinstance(result, str):
            try:
                data = json.loads(result)
                return data
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON from result")
                return None
        else:
            print("Error: result is not a string")
            return None
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        return None


def create_ics_event(summary: str, start: datetime, end: datetime):
    cal = Calendar()
    cal.add('prodid', '-//My Product//example.com//')
    cal.add('version', '2.0')

    event = Event()
    event.add('uid', 'some-unique-id@example.com')
    event.add('dtstamp', datetime.utcnow())
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('summary', summary)

    cal.add_component(event)
    return cal


def build_ical_from_description(event_description: str, current_timestamp: datetime, output_file_path: str = "event.ics"):
    try:
        # 1. Use LangChain to parse the event information
        parsed = parse_event_with_langchain(event_description, current_timestamp)
        if not parsed:
            raise ValueError("Failed to parse event description")

        summary = parsed.get('summary')
        start_str = parsed.get('start_time')
        end_str = parsed.get('end_time')

        if not summary or not start_str:
            raise ValueError("Missing required fields in parsed data")

        # 2. Convert these strings to datetimes relative to current_timestamp
        start_dt = parse(start_str, settings={'RELATIVE_BASE': current_timestamp})
        if start_dt is None:
            raise ValueError("Could not parse start time from description.")

        end_dt = parse(end_str, settings={'RELATIVE_BASE': current_timestamp})
        if end_dt is None:
            # If cannot parse end time, default to 1 hour after start
            end_dt = start_dt + timedelta(hours=1)

        # 3. Create iCalendar event
        cal = create_ics_event(summary, start_dt, end_dt)

        # 4. Write the ICS file to disk
        ics_content = cal.to_ical()
        with open(output_file_path, 'wb') as f:
            f.write(ics_content)
        print(f"ICS file created at {output_file_path}")
    except ValueError as e:
        print(f"Error creating event: {e}")
        # Return a more informative error message
        return {"error": str(e)}