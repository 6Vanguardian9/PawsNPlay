FROM python:3.11-slim

WORKDIR /app

RUN pip install uv
ENV UV_SYSTEM_PYTHON=1

COPY . .

RUN uv pip install fastapi uvicorn

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "app/app.py"]
