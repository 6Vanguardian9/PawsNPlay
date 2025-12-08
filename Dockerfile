FROM python:3.11-slim

WORKDIR /app

# Install UV first
RUN pip install uv
ENV UV_SYSTEM_PYTHON=1

# Copy dependency files first for better layer caching
COPY uv.lock requirements.txt ./

# Install dependencies from lockfile
RUN uv pip install -r requirements.txt

# Copy rest of application code
COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "app/app.py"]
