# How to run

## Build the docker image
```bash
docker build -t smart-cal-event-creator .
```

## Run the docker image
```bash
docker run -p 8000:8000 -p 11434:11434 --env-file .env smart-cal-event-creator
```