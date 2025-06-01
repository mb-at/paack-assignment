FROM python:3.11-slim

# Don’t create .pyc files and force stdout/stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy the entire src/ folder into /app/src
COPY src/ ./src

EXPOSE 8000

# 3) Default command to run Uvicorn on port 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
