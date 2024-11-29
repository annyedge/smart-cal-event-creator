import logging
from typing import Optional
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from app.models.ics_model import ICSAttributes # Pydantic model
import re


def parse_event_details(event_text: str) -> Optional[ICSAttributes]:
    if not event_text:
        logging.error("Event text is empty")
        return None

    try:
        # Initialize the PydanticOutputParser with your ICSAttributes model
        parser = PydanticOutputParser(pydantic_object=ICSAttributes)

        # Custom format instructions to prevent the LLM from outputting the schema
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

        # Construct the prompt
        prompt_template = PromptTemplate(
            template="""
Your task is to extract event details from the given text and return them as a JSON object matching the specified format.

Instructions:
{format_instructions}

Text:
"{event_text}"

Output:
""",
            input_variables=["event_text"],
            partial_variables={
                "format_instructions": format_instructions,
            },
        )

        # Initialize the language model with temperature set to 0
        ollama_llm = OllamaLLM(
            base_url="http://localhost:11434",
            model="llama3.2",  # Adjust the model name if necessary
            temperature=0,  # Set temperature to 0 for deterministic output
        )

        # Use OutputFixingParser to handle parsing errors
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=ollama_llm)

        # Create a chain using the Runnable interface
        chain = prompt_template | ollama_llm

        # Run the chain to get the LLM's raw output
        response = chain.invoke({"event_text": event_text})

        # Log the LLM's response for debugging
        logging.debug(f"LLM Response: {response}")

        # Attempt to extract JSON from the response
        try:
            # Use regex to extract JSON object from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON object found in LLM response.")
            json_str = json_match.group(0)

            # Parse the output using the fixing parser
            parsed_output = fixing_parser.parse(json_str)
        except Exception as e:
            logging.error(f"Failed to extract JSON from LLM output: {e}")
            return None

        # Validate and return the ICSAttributes object
        return parsed_output

    except Exception as e:
        logging.error(f"An error occurred while parsing event details: {e}")
        return None
