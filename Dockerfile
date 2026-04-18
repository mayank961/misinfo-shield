FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY data/ ./data/

RUN mkdir -p models/fake_news_model

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
