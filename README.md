# SCEC (Smart Calendar Event Creator)

This app will take your text input and create a calendar event for you.

## MacOS
On MacOS, it is recommended to run Ollama as a standalone application outside of Docker containers, as Docker Desktop does not support GPUs. Learn more: [Ollama Official Docker Image](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image).

### Install the Dependencies
1. Ensure Poetry is installed on your system. You can install it by following the instructions [here](https://python-poetry.org/docs/#installation).
2. Install the project dependencies:
```bash
poetry install
```
3. Activate the Poetry virtual environment:
```bash
poetry shell
```
4. Run the application:
```bash
poetry run uvicorn main:app --reload
```