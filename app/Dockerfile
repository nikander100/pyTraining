# Use a lightweight Python base
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port
EXPOSE 8008

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8008"]