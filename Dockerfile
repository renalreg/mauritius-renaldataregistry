FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m pip install -U pip

COPY docker-entrypoint.sh requirements.txt ./
COPY src ./src

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
