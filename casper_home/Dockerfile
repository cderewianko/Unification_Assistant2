

# Use slim Python 3.11 base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app/casper_home

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Default command to run your service
CMD ["python", "main.py"]
