FROM python:3.11-slim

ENV APP_HOME=/app  \
    PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR $APP_HOME
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt


COPY . ./

EXPOSE $PORT

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "$PORT"]