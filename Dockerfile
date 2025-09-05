FROM python:slim-bullseye

COPY . /home/

WORKDIR /home

RUN pip install -r requirements.txt

LABEL org.opencontainers.image.description="Squaddie"
LABEL org.opencontainers.image.authors="Niceygy (Ava Whale)"
LABEL org.opencontainers.image.source="https://github.com/Niceygy/Squaddie"

# Start 
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
