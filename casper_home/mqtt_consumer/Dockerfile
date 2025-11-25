

# Python base
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy consumer code
COPY . .

# Command to run consumer
CMD ["python", "mqtt_consumer.py"]
