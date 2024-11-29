# parser.py

import logging
from typing import Optional
import re

from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

from app.models.ics_model import ICSAttributes  # Your Pydantic model
from app.prompts.prompts import prompt_template, format_instructions  # Your prompt template


def parse_event_details(event_text: str) -> Optional[ICSAttributes]:
    if not event_text:
        logging.error("Event text is empty")
        return None

    try:
        # Initialize the PydanticOutputParser with your ICSAttributes model
        parser = PydanticOutputParser(pydantic_object=ICSAttributes)

        # Construct the prompt
        prompt = PromptTemplate(
            template=prompt_template,
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
        chain = prompt | ollama_llm

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
